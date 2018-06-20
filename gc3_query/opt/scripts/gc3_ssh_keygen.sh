#!/usr/bin/bash

echo "Enter region (eg. naac, apac, emea): "
read -e REGION
echo "Enter 4 digit project code (eg. cdmt, soar): "
read -e PROJECT_CODE
echo "Enter tag for the key (eg. 'admin' for opc/team access, 'cust' for keys given to projects for shell access to oracle, etc.): "
read -e SSH_KEY_TAG
echo "Enter SSH keystore password: "
read -e PASSWORD

export DATE=`date '+%Y%m%d'`
export KEY_FILE_BASE="${REGION}_${PROJECT_CODE}_${SSH_KEY_TAG}"
export PRIVATE_KEY_FILE="${KEY_FILE_BASE}.rsa"
export PUBLIC_KEY_FILE="${KEY_FILE_BASE}.rsa.pub"
export RENAMED_PUBLIC_KEY_FILE="${KEY_FILE_BASE}.pub"
export KEY_COMMENT="rsa-key_${REGION}-${PROJECT_CODE}_${DATE}"
export KEY_DIRECTORY="$PWD/key_store/$REGION/$PROJECT_CODE"
export PRIVATE_KEY_OUTPUT="${KEY_DIRECTORY}/${PRIVATE_KEY_FILE}"
export PUBLIC_KEY_OUTPUT="${KEY_DIRECTORY}/${PUBLIC_KEY_FILE}"
export RENAMED_PUBLIC_KEY_OUTPUT="${KEY_DIRECTORY}/${RENAMED_PUBLIC_KEY_FILE}"
export README_FILE="${KEY_DIRECTORY}/README.txt"

if [[ -e $PRIVATE_KEY_OUTPUT ]]
then
	echo 
	echo "********************************************************************************"
	echo "Keystore $PRIVATE_KEY_OUTPUT alredy exists!"
	echo "Remove or rename $PRIVATE_KEY_OUTPUT and retry, exiting."
	echo "********************************************************************************"
	echo 
	exit 1
fi

echo 
echo 
echo "Going to create 4096 byte RSA key: $PRIVATE_KEY_OUTPUT"
read -p "Enter [Yy] to continue: " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
	echo 
	echo "User input, $REPLY, was neither 'Y' or 'y', exiting."
	exit 1
	echo 
fi

if [ ! -d "${KEY_DIRECTORY}" ]
then
	echo 
	echo "Creating directory: $KEY_DIRECTORY"
	echo 
	mkdir -p $KEY_DIRECTORY
else
	echo 
	echo "Keystore directory already exists: $KEY_DIRECTORY"
	echo 
fi

echo "Creating RSA key-pair using password=\"$PASSWORD\" to $PRIVATE_KEY_OUTPUT"
echo 
ssh-keygen -b 4096 -t rsa -f $PRIVATE_KEY_OUTPUT -N $PASSWORD -C $KEY_COMMENT
echo 
echo "Moving $PUBLIC_KEY_OUTPUT to $RENAMED_PUBLIC_KEY_FILE"
mv $PUBLIC_KEY_OUTPUT $RENAMED_PUBLIC_KEY_OUTPUT



cat <<EOF >>$README_FILE
SSH keys created on $DATE
Region: $REGION
Project Code: $PROJECT_CODE
Password: $PASSWORD
Key Comment: $KEY_COMMENT
Key Size: 4096k


EOF



echo 
echo "Created private SSH key: $PRIVATE_KEY_OUTPUT"
echo "Created public SSH key: $RENAMED_PUBLIC_KEY_OUTPUT"
echo "Created README file: $README_FILE"
echo "Key Comment: $KEY_COMMENT"
echo 




echo "Done"
echo 
