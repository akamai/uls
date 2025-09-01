#!/bin/bash
TAG="testing"
TARGET_ARCH="linux/amd64"
cat << EOF
 ____  ____  ___        ________      ___      ___       __        __    _____  ___  ___________
("  _||_ " ||"  |      /"       )    |"  \    /"  |     /""\      |" \  (\"   \|"  \("     _   ")
|   (  ) : |||  |     (:   \___/      \   \  //   |    /    \     ||  | |.\\   \    |)__/  \\__/
(:  |  | . )|:  |      \___  \        /\\  \/.    |   /' /\  \    |:  | |: \.   \\  |   \\_ /
 \\ \__/ //  \  |___    __/  \\      |: \.        |  //  __'  \   |.  | |.  \    \. |   |.  |
 /\\ __ //\ ( \_|:  \  /" \   :)     |.  \    /:  | /   /  \\  \  /\  |\|    \    \ |   \:  |
(__________) \_______)(_______/      |___|\__/|___|(___/    \___)(__\_|_)\___|\____\)    \__|
EOF
## BUILD
echo -e "Building the ${TAG} tag for ULS \n\n\n"
docker build --platform ${TARGET_ARCH} -t akamai/uls:${TAG} .

### PUSH
echo -e "\n\n\nPUSHING the ${TAG} tag for ULS \n\n\n"
echo "Are you sure you want to push ? (N|y)"
read reply
if [ "$reply" == "y" ] ; then
  docker push akamai/uls:${TAG}
else
  echo "aborting push"
fi