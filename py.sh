echo "Enter python version (only number) you want to install. Example: 3.11.1"
read PYTHON_VERSION
#echo "Enter your system password"
#read PASSWORD
echo "Going to install python : " $PYTHON_VERSION

#echo $PASSWORD | sudo -S -k apt-get update

sudo apt-get update

sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev sqlite-devel libssl-dev libsqlite3-dev tk-dev libc6-dev libbz2-dev -y
sudo apt install zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libreadline-dev libffi-dev wget -y
sudo apt install figlet toilet -y
mkdir ~/python
cd ~/python

# check if file is already available.
# may be it was downloaded in the first attempt
# but our script failed and we are trying again.

filename=Python-$PYTHON_VERSION.tar.xz
if [[ -f "$filename" ]];
then
    echo "$filename has found. we will install python using this."
else
    echo "$filename has not been found"
    # download python
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz
fi


#extract python
tar -xf Python-$PYTHON_VERSION.tar.xz

# go to python folder
cd Python-$PYTHON_VERSION

# configure python
./configure --enable-loadable-sqlite-extensions --enable-optimizations


make
# altinstall will not replace the default python
sudo make altinstall

cd ..
# now we clean up
sudo rm -rf Python-$PYTHON_VERSION
sudo rm Python-$PYTHON_VERSION.tar.xz

# create python alias to python3.11


echo  "=========================================================="
figlet Python $PYTHON_VERSION
echo  "=========================================================="
echo "is installed"
alias py=python"${PYTHON_VERSION:0:4}"
echo "now you can use py instead of python${PYTHON_VERSION:0:4} to run your scripts"
