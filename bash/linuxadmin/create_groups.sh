# Create top level policies
sudo mkdir /home/common/policies
# Make file read only
chmod a=rx /home/common/policies

sudo groupadd temp
sudo groupadd staff
sudo groupadd developers
sudo groupadd admin

sudo mkdir -p /home/common/groups/temp
sudo mkdir    /home/common/groups/staff
sudo mkdir    /home/common/groups/developers
sudo mkdir    /home/common/groups/admin

sudo chgrp -R temp /home/common/groups/temp
sudo chgrp -R staff /home/common/groups/staff
sudo chgrp -R developers /home/common/groups/developers
sudo chgrp -R admin /home/common/groups/admin

sudo chmod -R 2775 /home/common/groups/temp
sudo chmod -R 2775 /home/common/groups/staff
sudo chmod -R 2775 /home/common/groups/developers
sudo chmod -R 2775 /home/common/groups/admin

# Make policy folder for each group
sudo mkdir -p /home/common/groups/temp/policies
sudo mkdir    /home/common/groups/staff/policies
sudo mkdir    /home/common/groups/developers/policies
sudo mkdir    /home/common/groups/admin/policies

# Make each policy folder read only
sudo chmod a=rx /home/common/groups/temp/policies
sudo chmod a=rx /home/common/groups/staff/policies
sudo chmod a=rx /home/common/groups/developers/policies
sudo chmod a=rx /home/common/groups/admin/policies

# Get the mount name 
mount=$(hostnamectl | awk -F ' ' '/Operating System:/ {print $1}')
# Get the format type
format=$(hostnamectl | awk -F ' ' '/Operating System:/ {print $2}')
# Get the OS name to determine what program to install
os=$(hostnamectl | awk -F ' ' '/Operating System:/ {print $3}')

if [ $os == "Ubuntu" ]
then
	# Get quota support
	sudo apt-get install quota
	# Install quota_v1.ko and quota_v2.ko dependencies
	sudo apt-get install linux-image-extra-virtual	
fi

if [ $os == "CentOS" ]
then
	# Get quota support
	sudo yum install quota
fi

# Find the line within /etc/fstab that contains the "/" mount, and print the line number
line_num=$(awk -F ' ' '$2 == "\/" {print NR}' /etc/fstab)
# Update "/" fstab mount to support user and group quotas
sudo sed -i "$line_num s/defaults/defaults,usrquota,grpquota/" /etc/fstab
# Remount disk with new quota rules
sudo mount -o remount /

# XFS partitions take special effort to support quotas
if [ $format == "xfs" ]
then
	# Install grub2 on the partition
	sudo grub2install $mount --skip-fs-probe
	# Configure grub
	sudo grub2-mkconfig -o /boot/efi/EFI/${os,,}/grub.cfg
	# Set the quota limit of temp group
	sudo xfs_quota -x -c 'limit -g bsoft=6144m bhard=8192m isoft=1000 ihard=1200 temp' /
	# Check the quota limits
	sudo quota -g temp
else
	# Run quotacheck to create aquota.group and aquota.user files
	sudo quotacheck -ugm /
	# Turn quota on
	sudo quotaon -v /
	# Set the quota limit to 10G for temp group
	sudo setquota -g temp 9G 10G 0 0 /
fi
