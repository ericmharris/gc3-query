# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

import os
import sys
import json
import logging 
import textwrap
from collections import OrderedDict
try:
    from utils import Utils, FormatText
    from messages import ErrorMessages, CatalogConstants
except:
    from .utils import Utils, FormatText
    from .messages import ErrorMessages, CatalogConstants

#======= CONSTANTS ==============================================================
NUM_PROP_LIST = 5
#======= CLASSES =================================================================


class OutputFormatter(object):
    """
       a generic formatter which needs to implemented in order to get the 
       desired output format specified in the conf file.
    """
    def __init__(self, content=None, \
                 cmd_dict=None, \
                 cmd_name=None, \
                 response_headers=None):
        self._cmd_dict = cmd_dict 
        self._content = content
        self._cmd_name = cmd_name
        self._response_headers = response_headers
        self._max_props = NUM_PROP_LIST
        self._utils = Utils()
    
    @property
    def content(self):
        return self._content
    
    def _format_content(self):
        raise NotImplementedError("Not Implemented")
    
    def _format_error_content(self):
        raise NotImplementedError("Not Implemented")

    def _parse_yaml_output(self, output_data):
        import yaml
        try:
            # if the response output is of type str and json compatible,
            # a json dict obj is returned, otherwise a string,
            # object is returned.
            output_data = yaml.load(output_data)
        except yaml.YAMLError as exc:
            logger.error("Error while parsing the input as yaml: %s", exc)
        except Exception as ex:
            logger.error("Response data is not an Yaml file: %s", ex)

        return output_data

class JSONFormatter(OutputFormatter):
    
    def _format_content(self):
        data = self.content
        # BUG FIX: 25350442, Convert YAML response output to json
        if not isinstance(data, (dict,list)):
            data = self._parse_yaml_output(data)
        # commented the sort keys. To maintain the order from the REST response
        json_formatted = json.dumps(data, indent=4, separators=(',',':')) #,sort_keys=True)
        return json_formatted
    
    def _format_error_content(self):
        data = self.content
        json_formatted = json.dumps(data, indent=4, separators=(',',':'))
        return json_formatted
        
class TextFormatter(OutputFormatter):
    
    def _format_content(self):
        # to replace any string if it has \r\n for linux
        data = self.content.replace('\r','') if self._utils.isLinux() else self.content
        return data 

class ConciseOutputFormatter(OutputFormatter):
        
    def _format_content(self):
        offset_data = self.content
        if CatalogConstants.OUTPUT_FILTER in self._cmd_dict and \
                        any(param in self._cmd_dict[CatalogConstants.OUTPUT_FILTER] for param in 
                            [CatalogConstants.INCLUDE_PROPERTIES, \
                            CatalogConstants.OFFSET]):
            try:
                output = None
                offset = False
                show_table = False
                property_list = None
                # if offset is given and the resulting value json for
                # the offset is a dict where the include properties are
                # present in the first level of the JSON - Typically for POST 
                parse_offset_first_level = False
                show_properties_dynamically = False
                # Read offset data for additional processing
                if CatalogConstants.OFFSET in self._cmd_dict[CatalogConstants.OUTPUT_FILTER]:
                    offset_data = offset_data[self._cmd_dict[CatalogConstants.OUTPUT_FILTER][CatalogConstants.OFFSET]]    
                    offset = True
                
                if CatalogConstants.SHOW_TABLE in self._cmd_dict[CatalogConstants.OUTPUT_FILTER]:
                    show_table = self._cmd_dict[CatalogConstants.OUTPUT_FILTER][CatalogConstants.SHOW_TABLE]
                
                if CatalogConstants.INCLUDE_PROPERTIES in self._cmd_dict[CatalogConstants.OUTPUT_FILTER]:
                    property_list = self._cmd_dict[CatalogConstants.OUTPUT_FILTER][CatalogConstants.INCLUDE_PROPERTIES]
                    # a special case, where include properties is [], then return empty
                    if len(property_list) == 0:
                        return EMPTY_STRING
                else:
                    # developmental time processing
                    property_list = range(self._max_props)
                    show_properties_dynamically = True
                # maintain the count. if counter is 1 show block
                # if counter is more than 1 then show table.
                counter = 0
                
                # limit the property list to max_props = 5 and if show as list is false
                # restrict the property list to max_props for table output. 
                if len(property_list) > self._max_props and show_table:
                    property_list = property_list[:self._max_props]
                
                if not offset and (len(offset_data) == 1 if isinstance(offset_data, list) else True):
                    # if offset_data was not through offset property.
                    concise_json = OrderedDict()
                    if isinstance(offset_data, list):
                        offset_data = offset_data[0]
                    
                    concise_json = self._populate_dict_for_short_output(show_properties_dynamically, \
                                                                        offset_data, property_list)
                    counter = 1
                    output = concise_json                   
                elif isinstance(offset_data, (dict,list)):
                    concise_list = []
                    # create a common iterable for dict and list
                    common_iterable = offset_data.keys() if isinstance(offset_data, dict) else range(len(offset_data))
                    # Loop over the common iterable to build the output.                                           
                    for index_key in common_iterable:
                        # custom rendering for commands like 'services' to show LS output
                        #if self._cmd_name in self._utils.specific_commands and isinstance(offset_data, (dict,list)):
                            #concise_list.append(index_key)
                        #    self._build_services_output(index_key, offset_data, property_list, concise_list)
                        if offset_data[index_key] and isinstance(offset_data[index_key], dict): 
                            temp_dict = self._populate_dict_for_short_output(show_properties_dynamically, \
                                                                             offset_data[index_key], property_list)
                            concise_list.append(temp_dict)
                            counter += 1
                        else:
                            # for POST requests
                            parse_offset_first_level = True
                            break      
                    if not concise_list and parse_offset_first_level:
                        temp_dict = self._populate_dict_for_short_output(show_properties_dynamically, \
                                                                        offset_data, property_list)
                        concise_list.append(temp_dict)
                    
                    output = concise_list
                    # sort only for services/apps
                    if self._cmd_name in self._utils.specific_commands and output:
                        output.sort(key = lambda user: user[property_list[0][CatalogConstants.INCLUDE_PROP_DISP_NAME]])
                        
                # invoke the appropriate format to display short output
                if counter <= 1 and not show_table:
                    return self._display_block_output(output)
                else:
                    if output:
                        return TableFormatter(content=output, initialSection=True, num_prop_list=len(property_list))._format_content()
                    else:
                        return ErrorMessages.OPAAS_CLI_NO_DATA_FOUND
                    
            except Exception as e:
                logger.error(ErrorMessages.OPAAS_CLI_SHORT_OUTPUT_PARSING_ERROR_DISPLAY.format(e))      
        
        # output filter is given but no offset / includeProperties:
        #by default, show the first level properties.
        return self._show_first_level_props(self.content)
    
    def _build_services_output(self, index_key, offset_data, property_list, concise_list):
        if isinstance(property_list, range):
            concise_list.append(index_key)
        else:
            if property_list[0][CatalogConstants.INCLUDE_PROP_NAME] in offset_data[index_key]:
                concise_list.append(offset_data[index_key][property_list[0][CatalogConstants.INCLUDE_PROP_NAME]])
    
    def _show_first_level_props(self, data):
        temp_dict = OrderedDict()
        if isinstance(data, dict):
            temp_dict =self._iterate_over_dict(data)
            return TableFormatter(content=temp_dict, initialSection=True)._format_content()
        elif isinstance(data, list):
            output = []
            for value in data:
                if value:
                    temp_dict = self._iterate_over_dict(value)
                    output.append(temp_dict)
            return TableFormatter(content=output, initialSection=True)._format_content()
        else:
            # by default return the Json formatted output
            return JSONFormatter(content=data)._format_content()
    
    def _iterate_over_dict(self, data_dict):
        temp_dict = OrderedDict()
        counter = 0
        for k,v in data_dict.items():
            if isinstance(v, (dict,list)):
                temp_dict[k] = self._utils._json_object
            else:
                # Check if the value is not None
                if v:
                    temp_dict[k] = v
                else:
                    temp_dict[k] = 'null'
            counter += 1
            if counter == self._max_props:
                break
        
        return temp_dict
            
    
    def _populate_dict_for_short_output(self, show_properties_dynamically, orig_op_dict, property_list):
        temp_dict = OrderedDict()
        if show_properties_dynamically:
            items = list(orig_op_dict.items())
            for num in property_list:
                key, value = items[num]
                temp_dict[key] = value
        else:
            for item in property_list:
                # check if the value is present.
                if item[CatalogConstants.INCLUDE_PROP_NAME] in orig_op_dict and \
                                            (orig_op_dict[item[CatalogConstants.INCLUDE_PROP_NAME]] or \
                                             orig_op_dict[item[CatalogConstants.INCLUDE_PROP_NAME]] == 0):
                    orig_value = orig_op_dict[item[CatalogConstants.INCLUDE_PROP_NAME]]
                    temp_dict[item[CatalogConstants.INCLUDE_PROP_DISP_NAME]] = self._convert_nested_json_to_name_value(orig_value) \
                                                                                if isinstance(orig_value, (dict,list)) else orig_value
                else:
                    if any(param in item[CatalogConstants.INCLUDE_PROP_NAME] for param in ['jobId', 'job_id']) \
                         and self._utils._location in self._response_headers:
                        # if jobId is a property to be shown for SHORT output, read from the location and display it,
                        # if it doesnt exist in the response json.
                        match = self._utils.get_job_id_from_location_header(self._response_headers[self._utils._location])
                        job_id = "N/A" if match is None else match.group('jobid')
                        temp_dict[item[CatalogConstants.INCLUDE_PROP_DISP_NAME]] = job_id
                    else:
                        temp_dict[item[CatalogConstants.INCLUDE_PROP_DISP_NAME]] = "N/A"
        
        return temp_dict
    
    def _convert_nested_json_to_name_value(self, value):
        if isinstance(value, list) and len(value) > 1:
            return self._utils._json_object
        if isinstance(value, list):
            value = value[0]
        data = "{0}".format(", ".join(["{0}: {1}".format(k, self._utils._json_object if isinstance(v, (dict, list)) else v) for k, v in value.items()]))
        return data
            
    
    def _display_block_output(self, output):
        if isinstance(output, dict):
            return self._format_block_output(output)
        elif isinstance(output, list):
            op_dict = output[0] if output else output
            if isinstance(op_dict, dict):
                return self._format_block_output(op_dict)
            else: 
                return self._format_block_output(output)
        # Return text formatted output as the output might be a string.
        return TextFormatter(content=output)._format_content()
    
    def _format_block_output(self, output):
        if output:
            maxlen = len(max(output, key=len))
            data = "\n".join(["    ".join([" {0}{1}".format(FormatText.bold(key + ":"), ((maxlen - len(key)) * ' ')), str(val)]) for key, val in output.items()])
        else:
            data = ErrorMessages.OPAAS_CLI_NO_DATA_FOUND
        return TextFormatter(content=data)._format_content()
        
        
class HtmlFormatter(OutputFormatter):
    def _format_content(self):
        data = self.content
        formatted_html = JsonToHtml().convert(self, json = data)
        return formatted_html if formatted_html is not None else data


class JsonToHtml(object):

    def convert(self, formatter, **args):
        '''
        convert json Object to HTML Table format
        '''
        # table attributes such as class
        # eg: table_attributes = "class = 'sortable table table-condensed table-bordered table-hover'
        global table_attributes
        table_attributes = ''
        htmlFormatter = formatter
        
        if 'table_attributes' in args:
            table_attributes = args['table_attributes']
        else:
            # by default HTML table border
            table_attributes = 'border="1"'

        if 'json' in args:
            self.json_input = args['json']
            if not isinstance(self.json_input, (dict,list)):
                # BUG FIX: 25350442. Convert YAML response output to html
                try:
                    self.json_input = htmlFormatter._parse_yaml_output(self.json_input)
                    # convert to str for html processing.
                    if isinstance(self.json_input, (dict, list)):
                        self.json_input = json.dumps(self.json_input)
                except:
                    pass
            else:
                self.json_input = json.dumps(self.json_input)
        else:
            raise Exception('Can\'t convert NULL!')

        try:
            # Reconverting the response string to maintain the properties order in the output.
            ordered_json = json.loads(self.json_input, object_pairs_hook=OrderedDict)
        except:
            # The json_input (which is the output) is a string and is not Json serializable
            logger.error("The response output cannot be converted to HTML.")
            return self.json_input
        
        # Fix for BUG 22506411 and 22760139: Added html parsing for List type Jsons.
        if not isinstance(ordered_json,(dict,list)):
            return ordered_json 
        
        # To sort the values in the json before converting to html.
        # commenting the HTML sorting too.
        #try:
        #    sorted_json = json.dumps(ordered_json, sort_keys=True)
        #    ordered_json = json.loads(sorted_json, object_pairs_hook=OrderedDict)
        #except:
        #    pass

        # this is invoked only if the response content is a type of dict, json or list. 
        return self.iterJson(ordered_json)

    def columnHeadersFromListOfDicts(self, ordered_json):
        '''
        If suppose some key has array of objects and all the keys are same,
        instead of creating a new row for each such entry, club those values,
        thus it makes more sense and more readable code.
        @example:
            jsonObject = {"sampleData": [ {"a":1, "b":2, "c":3}, {"a":5, "b":6, "c":7} ] }
            OUTPUT:
                <table border="1"><tr><th>1</th><td><table border="1"><tr><th>a</th><th>c</th><th>b</th></tr><tr><td>1</td>
                <td>3</td><td>2</td></tr><tr><td>5</td><td>7</td><td>6</td></tr></table></td></tr></table>
        '''

        if len(ordered_json) < 2:
            return None
        if not isinstance(ordered_json[0],dict):
            return None

        column_headers = ordered_json[0].keys()

        for entry in ordered_json:
            if not isinstance(entry,dict):
                return None
            if len(entry.keys()) != len(column_headers):
                return None
            for header in column_headers:
                if not header in entry:
                    return None
        return column_headers

    def iterJson(self, ordered_json):
        '''
        Iterate over the JSON and process it to generate the super awesome HTML Table format
        '''
        def markup(entry, parent_is_list = False):
            '''
            Check for each value corresponding to its key and return accordingly
            '''
            if(isinstance(entry,str)):
                return str(entry)
            if(isinstance(entry,int) or isinstance(entry,float)):
                return str(entry)
            if(parent_is_list and isinstance(entry,list)==True):
                #list of lists are not accepted
                return ''
            if(isinstance(entry,list)==True) and len(entry) == 0:
                return ''
            if(isinstance(entry,list)==True):
                return '<ul><li>' + '</li><p/><li>'.join([markup(child, parent_is_list=True) for child in entry]) + '</li><p/></ul>'
            if(isinstance(entry,dict)==True):
                return self.iterJson(entry)

            #safety: don't do recursion over anything that we don't know about - items() will most probably fail
            return ''
        
        def buildHtml(json_value, htmlOutput):
            for k,v in json_value.items():
                htmlOutput = htmlOutput + '<tr>'
                #htmlOutput = htmlOutput + '<th width="100%">'+ markup(k) +'</th>'
                # Transposing only the dictionary keys into separate rows.
                if isinstance(v, dict):
                    htmlOutput = htmlOutput + '<th colspan="2" align="center">'+ markup(k) +'</th>'
                    htmlOutput = htmlOutput + '</tr>'  
                else: 
                    htmlOutput = htmlOutput + '<th align="center">'+ markup(k) +'</th>'
                
                if (v == None):
                    v = str('')
                if(isinstance(v,list)):
                    column_headers = self.columnHeadersFromListOfDicts(v)
                    if column_headers != None:
                        htmlOutput = htmlOutput + '<td>'
                        htmlOutput = htmlOutput + table_init_markup
                        htmlOutput = htmlOutput + '<tr><th>' + '</th><th>'.join(column_headers) + '</th></tr>'
                        for list_entry in v:
                            htmlOutput = htmlOutput + '<tr><td>' + '</td><td>'.join([markup(list_entry[column_header]) for column_header in column_headers]) + '</td></tr>'
                        htmlOutput = htmlOutput + '</table>'
                        htmlOutput = htmlOutput + '</td>'
                        htmlOutput = htmlOutput + '</tr>'
                        continue
                # Transposing only the dictionary keys into separate rows.                    
                if isinstance(v, dict):
                    htmlOutput = htmlOutput + '<tr>'
                    htmlOutput = htmlOutput + '<td colspan="2" align="center">' + markup(v) + '</td>'
                else:
                    htmlOutput = htmlOutput + '<td align="center">' + markup(v) + '</td>' 
                #htmlOutput = htmlOutput + '<td>' + markup(v) + '</td>'
                htmlOutput = htmlOutput + '</tr>'      
            return htmlOutput
        
        htmlOutput = ''

        global table_attributes
        table_init_markup = "<table %s>" %(table_attributes)
        htmlOutput = htmlOutput + table_init_markup
        
        # Fix: Bug 22760139: added support for converting a list type json into html.
        if isinstance(ordered_json, list):
            for item in ordered_json:
                if (isinstance(item, dict)):
                    htmlOutput = htmlOutput + buildHtml(item, htmlOutput)
        else:
            htmlOutput = htmlOutput + buildHtml(ordered_json, htmlOutput)
                
        htmlOutput = htmlOutput + '</table>'
        return htmlOutput
        
class TableFormatter(OutputFormatter):
    '''
        Table Formatter which displays the JSON as a Table on the Console output.
    '''
    def __init__(self, content=None, initialSection=False, srv_name=None, num_prop_list=NUM_PROP_LIST):
        '''
            @type initialSection : bool
            @param initialSection : create a default section in the psmTable
        '''
        self._srv_name = srv_name
        super().__init__(content=content)
        self._psmtable = PSMTable(initial_section=initialSection,
                                  column_separator = ' ', num_prop_list=num_prop_list)
        
    def _format_content(self):
        if isinstance(self._content, (list, dict)):
            if self._build_table(self._srv_name, self._content):
                try:
                    self._psmtable.display()
                except Exception as e:
                    # if exception, then we can ignore.
                    pass
                    # print(str(e))
                return EMPTY_STRING
        return self._content
    
    def _build_table(self, title, content, indent_level=0):
        # Recursively invoke the build_table to build the table from the given
        # content, which can be a dict or list of dicts. 
        if title is not None:
            self._psmtable.new_section(title, indent_level) 
        if not content:
            return False
        
        if isinstance(content, list):
            if isinstance(content[0], dict):
                self._build_table_from_list(title, content, indent_level)
            else:
                for item in content:
                    if self._isQuantifiable(item):
                        self._psmtable.add_section_rows([item])
                    elif all(self._isQuantifiable(el) for el in item):
                        self._psmtable.add_section_rows(item)
                    else:
                        self._build_table(title=None, content=item)
        elif isinstance(content, dict):
            self._build_table_from_dict(content, indent_level) 
        
        return True
    
    def _build_table_from_list(self, title, current_dict, indent_level):
        headers, nested = self._parse_single_nested_value_keys_from_list(current_dict)
        self._psmtable.add_section_header(headers)
        first = True
        for element in current_dict:
            if not first and nested:
                self._psmtable.new_section(title,
                                       indent_level=indent_level)
                self._psmtable.add_section_header(headers)
            first = False
            # Use get() to account for the fact that sometimes an element
            # may not have all the keys from the header.
            self._psmtable.add_section_rows([element.get(header, '') for header in headers])
            for nested_key in nested:
                # Some of the attributes may not be in every single element of the list, so we need to
                # check this condition before recursing.
                if nested_key in element:
                    self._build_table(nested_key, element[nested_key],
                                    indent_level=indent_level + 1)    
                    
    def _build_table_from_dict(self, current_dict, indent_level):
        # parse the current dicts key/value into header / row values
        # if its a single key-value. if the value is a list of dict or
        # another dict, recursively call the build table.
        headers, nested_headers = self._parse_single_nested_value_keys(current_dict)
        #if len(headers) == 1:
            # if a dict has a single key/value pair.
        #    self._psmtable.add_section_rows([headers[0], current_dict[headers[0]]])
        if headers:
            # Add the headers and its values (into rows) 
            self._psmtable.add_section_header(headers)
            self._psmtable.add_section_rows([current_dict[k] for k in headers])
        for nested_key in nested_headers:
            # Call the build table to parse the nested dicts into table.
            self._build_table(nested_key, current_dict[nested_key],
                              indent_level = indent_level + 1)
    
    def _parse_single_nested_value_keys_from_list(self, list_of_dicts):
        # We want to make sure we catch all the keys in the list of dicts.
        # Most of the time each list element has the same keys, but sometimes
        # a list element will have keys not defined in other elements.
        headers = OrderedDict()
        nested = OrderedDict()
        for item in list_of_dicts:
            current_headers, current_nested = self._parse_single_nested_value_keys(item)
            # USING orderedDict to maintain order of the element.
            #headers.update(current_headers)
            for item in current_headers:
                headers[item] = None
            #nested.update(current_nested)
            for elem in current_nested:
                nested[elem] = None
        #headers = list(sorted(headers))
        #nested = list(sorted(nested))
        headers = headers.keys() #list(headers)
        nested = nested.keys() #nested = list(nested)
        return headers, nested
    
    def _parse_single_nested_value_keys(self, current_dict):
        # Parse the current dict into headers with just the value
        # and into nested headers which has a value that can be 
        # a list of dicts or dict
        headers = []
        nested = []
        for item in current_dict:
            if self._isQuantifiable(current_dict[item]):
                headers.append(item) 
            else:
                nested.append(item)
        
        return headers, nested
        
    def _isQuantifiable(self, value):
        # Sometimes the value can a dict or list of dict.
        # hence we need to build a table for those values.
        # Return True if its a single key value pair.
        return not isinstance(value, (list, dict)) 

class PSMTable(object):
    '''
        PSM Table
    '''
    def __init__(self, initial_section=False, column_separator = ' ', num_prop_list=NUM_PROP_LIST):
        self._table_utils = TableUtils(num_prop_list=num_prop_list)    
        if initial_section:
            self._current_section = PSMTableSection(self._table_utils)
            self._all_sections = [self._current_section]
        else: 
            self._all_sections = []
            self._current_section = None
        self._column_separator = column_separator   
        self._terminal_width_size = self._table_utils.get_terminal_size
    
    def add_section_title(self, title):
        # Add the title to the current section
        self._current_section.title = title
        
    def add_section_header(self, headers):
        # add the headers for that section and indent level
        self._current_section.headers = headers 
    
    def add_section_rows(self, rows):
        # add the values into the rows.
        self._current_section.rows = rows 
    
    def new_section(self, title, indent_level=0):
        self._current_section = PSMTableSection(self._table_utils)
        self._all_sections.append(self._current_section)
        self._current_section.title = title
        self._current_section.indent_level = indent_level
    
    def display(self):
        # Display the table on the console output
        max_width = self._calculate_max_width() #self._terminal_width_size #
        convert_table = self._determine_conversion_needed(max_width)
        if convert_table:
            self._table_utils.convert_to_vertical_table(self._all_sections)
            max_width = self._calculate_max_width()
            if max_width > self._terminal_width_size:
                # if the max width is still greater than calculate manually
                if (self._terminal_width_size - 80) >= 40:
                    max_width = 80 + 40
                else:    
                    max_width = self._terminal_width_size
        
        # Comment the below line, as of now we are not showing the first level key as header.        
        #sys.stdout.write('-' * max_width + '\n')
        for section in self._all_sections:
            self._display_section(section, max_width)
        
    def _determine_conversion_needed(self, max_width):
        # If we don't know the width of the controlling terminal,
        # then we don't try to resize the table.
        # print("Max_width: ", max_width)
        # print("Terminal_width: ", self._terminal_width_size)
        if max_width > self._terminal_width_size:
            return True
            #return False
                    
    def _calculate_max_width(self):
        # Calculate the max width of the rows / headers for building the table.
        max_width = max(s.total_widths(padding=2, with_border=True,
                                      outer_padding=s.indent_level)
                        for s in self._all_sections)
        return max_width
    
    def _display_section(self, table_section, max_width):
        stream = TableOutputStream(table_section.indent_level,
                                ' ',' ')
        max_width -= (table_section.indent_level * 2)
        self._parse_and_display_title(table_section, max_width, stream)
        self._parse_and_display_column_titles(table_section, max_width, stream)
        self._parse_and_display_rows(table_section, max_width, stream)
    
    def _parse_and_display_title(self, section, max_width, stream):
        # The title example
        #     title      
        # ---------------
        if section.title:
            title = section.title
            if title is not None and title:
                stream.write(self._table_utils.center_text(title, max_width, ' ', ' ',
                                                           len(section.title)) + '\n')
            if not section.headers and not section.rows:
                stream.write(' %s ' % ('-' * (max_width - 2)) + '\n')
                
    def _parse_and_display_column_titles(self, section, max_width, stream):
        if not section.headers:
            return
        # In order to parse the column titles we need to know
        # the width of each of the columns.
        widths = section.calculate_column_widths(padding=3,
                                                 max_width=max_width)
        current = ''
        length_so_far = 0
        # The first cell needs both left and right edges '  header  '
        # while subsequent cells only need right edges '  header  '.
        first = True
        for width, header in zip(widths, section.headers):
            if first:
                left_edge = ' ' 
            else:
                left_edge = ''
            current += self._table_utils.align_left_header(text=FormatText.bold(header), length=width,
                                   left_edge=left_edge, right_edge=' ',
                                   text_length=len(header), first=first)
            if first:
                first = False
            length_so_far += width
        # commenting for printing concise table formate
        #self._write_line_break(stream, widths)
        stream.write(current + '\n')

    def _write_line_break(self, stream, widths):
        # write something like: ' ------- --------- '
        parts = []
        first = True
        for width in widths:
            if first:
                parts.append(' %s ' % ('-' * (width - 2)))
                first = False
            else:
                parts.append('%s ' % ('-' * (width - 1)))
        parts.append('\n')
        stream.write(''.join(parts))

    def _parse_and_display_rows(self, section, max_width, stream):
        # The first cell needs both left and right edges '  value  ' 
        # while subsequent cells only need right edges '  value   '.
        if not section.rows:
            return
        widths = section.calculate_column_widths(padding=3,
                                                 max_width=max_width)
        if not widths:
            return
        # to print line break if rows was values from a list.
        print_line_break_list = 0
        #self._write_line_break(stream, widths)
        for row in section.rows:
            # if the row is of nested list type iterate over 
            # the row to parse the header and value of the row
            if isinstance(row[0], list):
                print_line_break_list += 1 
                for el in row:
                    current = ''
                    length_so_far = 0
                    first = True
                    for width, element in zip(widths, el):
                        if first:
                            left_edge = ' '
                        else:
                            left_edge = ''
                        current = self._table_utils.align_left(text=str(element), length=width,
                                              left_edge=left_edge,
                                              right_edge= self._column_separator,
                                              text_length= len(str(element)),
                                              left_padding = 0,
                                              length_so_far=length_so_far,
                                              current=current,
                                              first=first)
                        length_so_far += width
                        if first:
                            first = False
                    self._write_to_stream(stream, current)
                # Comment for concise output
                #if print_line_break_list != len(section.rows) and len(section.rows) != 1:
                #    self._write_line_break(stream, widths)
            else:
                current = ''
                length_so_far = 0
                first = True
                for width, element in zip(widths, row):
                    if first:
                        left_edge = ' '
                    else:
                        left_edge = ''
                    current = self._table_utils.align_left(text=str(element), length=width,
                                          left_edge=left_edge,
                                          right_edge=self._column_separator,
                                          text_length= len(str(element)),
                                          left_padding = 0,
                                          length_so_far=length_so_far,
                                          current=current,
                                          first=first)
                    length_so_far += width
                    if first:
                        first = False
                self._write_to_stream(stream, current)
        # Comment for concise output format
        #self._write_line_break(stream, widths)
    
    def _write_to_stream(self, stream, current):
        if isinstance(current, list):
            stream.write(current)
        else:
            stream.write(current + '\n')
                                       
class PSMTableSection(object):
    '''
        A wrapper class which wraps the header and row information for a particular Section.
        A section holds, title, headers and rows for a particular Key/value pair in a dict.
        The values can be a single value or if the value is again a dict another inner section
        is created to hold the values.
    '''
    def __init__(self, table_util):
        self._rows = []
        self._headers = []
        self._title = ''
        self._indent_level = 0
        self._max_widths_headers_rows = []
        self._no_of_cols_one_row = None
        self._table_util = table_util
      
    @property
    def title(self):
        return self._title
    
    @title.setter 
    def title(self, title):
        self._title = title
  
    @property 
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers 
        self._update_max_widths(headers)
            
    @property 
    def rows(self):
        return self._rows   
    
    @rows.setter 
    def rows(self, row):
        self._rows.append(row)
        self._update_max_widths(row)  
    
    @property
    def indent_level(self):
        return self._indent_level
    
    @indent_level.setter 
    def indent_level(self, indent_level):
        self._indent_level = indent_level
        
    def _update_max_widths(self, row):
        # This is to calculate the max width of the header and corresponding
        # header value in the row. Store the one that is maximum of the two.
        if not self._max_widths_headers_rows:
            if self._isNestedLists(row):
                for elem_list in row:
                    if not self._max_widths_headers_rows:
                        self._max_widths_headers_rows = [len(str(el)) for el in elem_list]
                    else:
                        for i, el in enumerate(elem_list):
                            self._max_widths_headers_rows[i] = max(len(str(el)), self._max_widths_headers_rows[i])
            else:
                self._max_widths_headers_rows = [len(str(el)) for el in row]
        else:
            if self._isNestedLists(row):
                for elem_list in row:
                    for i, el in enumerate(elem_list):
                        self._max_widths_headers_rows[i] = max(len(str(el)), self._max_widths_headers_rows[i])
            else:
                for i, el in enumerate(row):
                    self._max_widths_headers_rows[i] = max(len(str(el)), self._max_widths_headers_rows[i])
        
        if self._max_widths_headers_rows:
            iter_range = range(len(self._max_widths_headers_rows))
            for i in iter_range:
                if self._max_widths_headers_rows[i] > self._table_util.get_row_max_width: #ROW_MAX_WIDTH:
                    self._max_widths_headers_rows[i] = self._table_util.get_row_max_width #ROW_MAX_WIDTH
    
    def _isNestedLists(self, content):
        for elem in content:
            if isinstance(elem, list):
                return True
        return False                    
    
    def calculate_column_widths(self, padding=0, max_width=None):
        # postcondition: sum(widths) == max_width
        unscaled_widths = [w + padding for w in self._max_widths_headers_rows]
        if max_width is None:
            return unscaled_widths
        if not unscaled_widths:
            return unscaled_widths
        else:
            # Compute scale factor for max_width.
            scale_factor = max_width / float(sum(unscaled_widths))
            scaled = [int(round(scale_factor * w)) if w >= 25 and scale_factor >= 1 else w for w in unscaled_widths]
            # Once we've scaled the columns, we may be slightly over/under
            # the amount we need so we have to adjust the columns.
            diff = sum(scaled) - max_width            
            while diff != 0:
                iter_order = range(len(scaled))
                #if diff < 0:
                #    iter_order = reversed(iter_order)
                for i in iter_order:
                    if diff > 0:
                        scaled[i] -= 1
                        diff -= 1
                    else:
                        scaled[i] += 1
                        diff += 1
                    if diff == 0:
                        break
                
            return scaled

    def total_widths(self, padding=0, with_border=False, outer_padding=0):
        total = 0
        # One char on each side == 2 chars total to the width.
        # changed border padding to 0. as we have removed the border
        border_padding = 0
        for w in self.calculate_column_widths():
            total += w + padding
        if with_border:
            total += border_padding
        total += outer_padding + outer_padding
        return max(len(self._title) + border_padding + outer_padding +
                   outer_padding, total)
    
    def __repr__(self):
        return ("PSMTableSection(title=%s, headers=%s, indent_level=%s, no_of_rows=%s)" %
                (self._title, self._headers, self._indent_level, len(self._rows)))

class TableOutputStream(object):
    def __init__(self, indent_level, left_indent_char=' ',
                 right_indent_char=' '):
        self._stream = sys.stdout
        self._indent_level = indent_level
        self._left_indent_char = left_indent_char
        self._right_indent_char = right_indent_char

    def write(self, text):
        if isinstance(text, list):
            for te in text:
                self._stream.write(self._left_indent_char * self._indent_level)
                self._stream.write(te)
                self._stream.write(self._right_indent_char * self._indent_level)
                self._stream.write('\n')
        else:
            self._stream.write(self._left_indent_char * self._indent_level)
            if text.endswith('\n'):
                self._stream.write(text[:-1])
                self._stream.write(self._right_indent_char * self._indent_level)
                self._stream.write('\n')
            else:
                self._stream.write(text)
            
class TableUtils(object):
    
    def __init__(self, num_prop_list=NUM_PROP_LIST):
        self._terminal_width_size = self.getTerminalSize()
        self._row_max_width = round(self._terminal_width_size / num_prop_list) if self._terminal_width_size else ROW_MAX_WIDTH
        self._row_wrap_width = self._row_max_width - 3
    
    @property 
    def get_terminal_size(self):
        return self._terminal_width_size
    
    @property
    def get_row_max_width(self):
        return self._row_max_width
    
    def getTerminalSize(self):
        default_width = 80
        try:
            import shutil
            size = shutil.get_terminal_size(fallback=(80,24))
            if size.columns and size.columns != 0:
                return size.columns
        except:
            logger.debug("Returning default Terminal Width: %s.\n" % default_width)
        return default_width
        
    def getTerminalSizeOLD(self):
        '''
            Returns the width of the Terminal. Based on the size of the terminal 
            build the Table.
        '''
        env = os.environ
        def ioctl_GWINSZ(fd=sys.stdout):
            default_width = 80
            try:
                import struct
                from fcntl import ioctl
                from termios import TIOCGWINSZ
                #h, w = struct.unpack('hh', ioctl(fd, TIOCGWINSZ,'1234'))[:2]
                h, w = struct.unpack('hhhh', ioctl(fd, TIOCGWINSZ, '\0' * 8))[:2]
            except Exception as e:
                #logger.debug("Exception while determining the size of the terminal width: %s\n" % str(e))
                return 0, default_width
            return h, w
        height, width = ioctl_GWINSZ()
        # return the width of the terminal.
        return width
    
    def center_text(self, text, length=80, left_edge=' ', right_edge=' ',
                text_length=None):
        '''
            Center text with specified edge chars.
    
            You can pass in the length of the text as an arg, otherwise it is computed
            automatically for you. center a string not based
            on it's length.
        '''
        if text_length is None:
            text_length = len(text)
        output = []
        char_start = (length // 2) - (text_length // 2) - 1
        output.append(left_edge + ' ' * char_start + text)
        length_so_far = len(left_edge) + char_start + text_length
        right_side_spaces = length - len(right_edge) - length_so_far
        output.append(' ' * right_side_spaces)
        output.append(right_edge)
        final = ''.join(output)
        return final
    
    def align_left_header(self, text, length=80, left_edge=' ', right_edge=' ',
                text_length=None, first=False):
        if text_length is None:
            text_length = len(text)
        output = []
        char_start = (length // 2) - (text_length // 2) - 1
        output.append(left_edge + text)
        if first:
            length_so_far = text_length
        else:
            length_so_far = len(left_edge) + text_length
        right_side_spaces = length - len(right_edge) - length_so_far
        output.append(' ' * right_side_spaces)
        output.append(right_edge)
        final = ''.join(output)
        return final
    
    def convert_to_vertical_table(self, sections):
        # Horizontal table to vertical table
        for i, section in enumerate(sections):
            if len(section.rows) >= 1 and section.headers:
                headers = section.headers
                new_section = PSMTableSection()
                new_section.title = section.title
                new_section.indent_level = section.indent_level
                if len(section.rows) == 1:
                    for header, element in zip(headers, section.rows[0]):
                        new_section.rows = [header, element]
                else:
                    # if the rows consists of nested list. process it accordingly
                    for row in section.rows:
                        list_of_list_values = []
                        for header, element in zip(headers, row):
                            list_of_list_values.append([header, element])
                        new_section.rows = list_of_list_values
                sections[i] = new_section

    def align_left(self, text, length, left_edge=' ', right_edge=' ', text_length=None,
                   left_padding=2, length_so_far=0, current='', first=False):
        # align the text to left in the row header and value
        if text_length is None:
            text_length = len(text)
        if text_length > self._row_max_width:
            text = text[:self._row_wrap_width] + '...'
            text_length = len(text)
        computed_length = (
            text_length + left_padding + len(left_edge) + len(right_edge))
        output = []
        addtional_calc = False
        if length - computed_length >= 0:
            padding = left_padding
        else:
            padding = 0
        if text_length > length:
            addtional_calc = True
        if addtional_calc:
            # Additional formatting if the length of the text is greater than the scaled column width.
            # scale_value is a number assumed in order to add left and righ padding.
            scale_value = 6
            padding = 2
            output_split = self._split_by_length(text, (length - scale_value)) 
            add_left_edge = False
            for te in output_split:
                output_formatted = []
                length_added = 0
                if add_left_edge:
                    # Append | and length so far to accomodate the row header place holder
                    # for multiple lines of text.
                    output_formatted.append(' ')
                    # length_so_far - 2: as we are adding left and right edge for 
                    # the place holder value of row header
                    output_formatted.append(' ' * (length_so_far - 2))
                    # append the border of the row value with left edge = ' '
                    output_formatted.append(' ')
                else:
                    # the length of current can be ignored in calculation.
                    if isinstance(current, list):
                        # will always be the row header and hence only one value in the list.
                        current = current[0]
                    output_formatted.append(current)
                    output_formatted.append(left_edge)
                    if not first:
                        length_added += len(left_edge)
                output_formatted.append(' ' * padding)
                length_added += padding
                output_formatted.append(te)
                length_added += len(te)
                output_formatted.append(' ' * (length - length_added - len(right_edge)))
                output_formatted.append(right_edge)
                
                output.append(''.join(output_formatted)) 
                add_left_edge = True
            return output
        else:
            length_added = 0
            output.append(left_edge)
            if not first:
                length_added += len(left_edge)
            output.append(' ' * padding)
            length_added += padding
            output.append(text)
            length_added += text_length
            output.append(' ' * (length - length_added - len(right_edge)))
            output.append(right_edge)
            current += ''.join(output)

        return current 
    
    def _split_by_length(self, text, length):
        w=[]
        n=len(text)
        for i in range(0,n,length):
            w.append(text[i:i+length])
        return w          

#======= CONSTANTS ===============================================================
OUTPUT_FORMATTER = {
    'json' : JSONFormatter,
    'text' : TextFormatter,
    'html' : HtmlFormatter,
    'short' : ConciseOutputFormatter,
    'table' : TableFormatter
}

ROW_MAX_WIDTH = 20 
ROW_WRAP_WIDTH = ROW_MAX_WIDTH - 3 
EMPTY_STRING = ""
logger = logging.getLogger(__name__)