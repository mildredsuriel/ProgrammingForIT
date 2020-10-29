# Create top level policies
sudo mkdir /home/ubuntu/policies
# Make file read only
chmod a=rx /home/ubuntu/policies

sudo groupadd temp
sudo groupadd staff
sudo groupadd developers
sudo groupadd admin

sudo mkdir -p /home/ubuntu/groups/temp
sudo mkdir    /home/ubuntu/groups/staff
sudo mkdir    /home/ubuntu/groups/developers
sudo mkdir    /home/ubuntu/groups/admin

sudo chgrp -R temp /home/ubuntu/groups/temp
sudo chgrp -R staff /home/ubuntu/groups/staff
sudo chgrp -R developers /home/ubuntu/groups/developers
sudo chgrp -R admin /home/ubuntu/groups/admin

sudo chmod -R 2775 /home/ubuntu/groups/temp
sudo chmod -R 2775 /home/ubuntu/groups/staff
sudo chmod -R 2775 /home/ubuntu/groups/developers
sudo chmod -R 2775 /home/ubuntu/groups/admin

# Make policy folder for each group
sudo mkdir -p /home/ubuntu/groups/temp/policies
sudo mkdir    /home/ubuntu/groups/staff/policies
sudo mkdir    /home/ubuntu/groups/developers/policies
sudo mkdir    /home/ubuntu/groups/admin/policies

# Make each policy folder read only
sudo chmod a=rx /home/ubuntu/groups/temp/policies
sudo chmod a=rx /home/ubuntu/groups/staff/policies
sudo chmod a=rx /home/ubuntu/groups/developers/policies
sudo chmod a=rx /home/ubuntu/groups/admin/policies

# Get quota support
sudo apt-get install quota
# Install quota_v1.ko and quota_v2.ko dependencies
sudo apt-get install linux-image-extra-virtual
# Update fstab to support user and group quotas
sudo sed -i '1 s/defaults/usrquota,grpquota/' /etc/fstab
# Remount disk with new quota rules
sudo mount -o remount /
# Run quotacheck to create aquota.group and aquota.user files
sudo quotacheck -ugm /
# Turn quota on
sudo quotaon -v /
# Set the quota limit to 10G for temp group
sudo setquota -g temp 9G 10G 0 0 /