# Front-End-New
SmartPlanting front_end
## Get Started: 
### 0. Important Notice
1. It is highly recommended to use Linux (Ubantu20.04 / Ubantu22.04)
2. Install basic Linux tools using (`make`, `gcc`, `curl`, `git`, etc.)
```shell
sudo apt install -y make gcc curl git
```
### 1. Clone this repo
#### (1) Make sure `git lfs` is installed
```shell
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install
```
#### (2) Clone with `git lfs`
```shell
git clone https://github.com/VisionX-FullStack/Front-End-New smartPlanting
git lfs pull     # Usually takes long...
```
### 2. Set up MongoDB
#### (1) Install MongoDB in Linux
```shell
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -    # should output "OK"
apt-key list
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
```
#### (2) Test your Installation
```shell
sudo systemctl start mongod.service
sudo systemctl status mongod      # "active (running)" in green text
sudo systemctl enable mongod
sudo apt-get install -y mongodb-clients
mongo --eval 'db.runCommand({ connectionStatus: 1 })'   # output json should contain ' "ok" : 1 '
```
### 3. Install dependencies
#### (1) Set up virtual Environment
##### (I) Install Anaconda
```shell
cd ~
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh   # Press ENTER until prompted to type "yes"
conda init
echo $PATH | grep conda          # Make sure "conda" is in your $PATH variable
source .bashrc                   # should see "(bash)" in front of your username
```
##### (II) Create a new virtual Environment
```shell
cd smartPlanting
conda create -n smartPlanting python=3.9      # yolov5 works only in python3.9!
conda activate smartPlanting
```
#### (2) Install packets under the virtual environment
##### (I) General
```shell
python -m pip install -r requirements.txt
```
##### (II) Deep learning
###### Pytorch
For CPU inference
```shell
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu  
```
For GPU training, check your CUDA version!
```shell
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116   # for CUDA 11.6
```
###### Others
```shell
cd main/views/yolov5_optimized
python -m pip install -r requirements.txt
```
### 4. Start Django!
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000       # use CTRL-C to exit
```
Then open https://127.0.0.1:8000 (or replace with the public IP address of your cloud server if you have one)!
### AWS info:
```txt
Public IPv4 address
54.177.214.223

User name
ubuntu

GitHub remote url address
https://github.com/VisionX-FullStack/Front-End
```

### AWS instruction:
```shell
git remote -v             # 检查远程仓库地址
git fetch origin main     # 下载远程仓库版本到本地仓库
git status                # 检查本地版本与远程版本在版本树中的区别
git diff origin           # 查看本地暂存区和工作区的区别
git stash                 # 将工作区继上一次提交后的修改内容移出并储存
git merge origin/main     # 将本地仓库中刚下载的版本合并到工作区
git stash pop             # 将之前储存的修改内容取出
git add .                 # 将所有修改添加到暂存区
git commit -m "update message" --author="name <email address>"  # 将本地暂存区内容添加到本地仓库中，记得添加更新简介和上传者名字
git pull                  # 以防在上述过程中远程仓库有新的提交而产生冲突，下载远程仓库版本并合并到工作区如果有冲突会提示
git push                  # 上传本地代码版本到远程仓库并合并

# 大文件传输（git单个文件要小于100M）
git lfs track *.pt                                      # 将所有xxx.pt文件视为大文件，用lfs方式传输
git add path/to/your/project/.gitattribute
git push <Remote Name> <Remote Branch>
# -------------------------------------------------------------------------------------------------
sudo systemctl restart nginx
```
