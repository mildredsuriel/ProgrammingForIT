# Get the OS name to determine what program to install
os=$(hostnamectl | awk -F ' ' '/Operating System:/ {print $3}')

# Create a directory to send all the logs to
mkdir network_logs

# Centos uses python for speedtest, while other OSes use the installed package
if [ $os == "CentOS" ]
then
	# Grab the python file
	wget -O speedtest-cli https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
	# Make the python file executable
	chmod +x speedtest-cli
	# Run the python file
	python3 speedtest-cli | tee network_logs/speedtest.log
	# Clean up the python file once done
	rm -rf speedtest-cli
else
	if [ -z "$(which speedtest-cli)" ]
	then
		echo "speedtest-cli not installed, installing..."
		#sudo apt install speedtest-cli -y
	fi
	speedtest-cli | tee network_logs/speedtest.log
fi

# save the ip address output to a log
ip address | tee network_logs/ip_address.log
# save the DNS output to a log
nslookup google.com | tee network_logs/dns.log
# save the open ports output to a log
sudo ss -tule | tee network_logs/open_ports.log
