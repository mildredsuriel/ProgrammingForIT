# Create top level policies
sudo mkdir -p /home/shared/policies
# Make file read only
sudo chmod a=rx /home/shared/policies

sudo groupadd temp
sudo groupadd staff
sudo groupadd developers
sudo groupadd admin

sudo mkdir -p /home/shared/groups/temp
sudo mkdir    /home/shared/groups/staff
sudo mkdir    /home/shared/groups/developers
sudo mkdir    /home/shared/groups/admin

sudo chgrp -R temp /home/shared/groups/temp
sudo chgrp -R staff /home/shared/groups/staff
sudo chgrp -R developers /home/shared/groups/developers
sudo chgrp -R admin /home/shared/groups/admin

sudo chmod -R 2775 /home/shared/groups/temp
sudo chmod -R 2775 /home/shared/groups/staff
sudo chmod -R 2775 /home/shared/groups/developers
sudo chmod -R 2775 /home/shared/groups/admin

# Make policy folder for each group
sudo mkdir -p /home/shared/groups/temp/policies
sudo mkdir    /home/shared/groups/staff/policies
sudo mkdir    /home/shared/groups/developers/policies
sudo mkdir    /home/shared/groups/admin/policies

# Make each policy folder read only
sudo chmod a=rx /home/shared/groups/temp/policies
sudo chmod a=rx /home/shared/groups/staff/policies
sudo chmod a=rx /home/shared/groups/developers/policies
sudo chmod a=rx /home/shared/groups/admin/policies

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
# Get the mount name 
mount=$(awk -F ' ' '$2 == "\/" {print $1}' /etc/fstab)
# Get the format type
format=$(awk -F ' ' '$2 == "\/" {print $3}' /etc/fstab)

# Update "/" fstab mount to support user and group quotas
sudo sed -i "$line_num s/defaults/defaults,usrquota,grpquota/" /etc/fstab
# Remount disk with new quota rules
sudo mount -o remount /

# XFS partitions take special effort to support quotas
if [ $format == "xfs" ]
then
	# Install grub2 on the partition
	sudo grub2-install $mount --skip-fs-probe
	# Configure grub
	sudo grub2-mkconfig -o /boot/efi/EFI/${os,,}/grub.cfg
else
	# Run quotacheck to create aquota.group and aquota.user files
	sudo quotacheck -ugm /
fi

# Turn quota on
sudo quotaon -v /
# Set the quota limit to 10G for temp group
sudo setquota -g temp 9G 10G 0 0 /
