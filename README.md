## Create python venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install email_validator
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install python-multipart
pip install pymysql
#pip install python-magic
pip install python-slugify
pip install web3
pip install mangum
```

**Use python venv**

```bash
source venv/bin/activate
uvicorn main:app --reload
```

## Install AWS SAM

```commandline
pip install aws
```

```bash
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
sam --version
rm -rf sam-installation aws-sam-cli-linux-x86_64.zip
```

Url de ejemplo

https://wquv3hlp9i.execute-api.eu-west-3.amazonaws.com/Prod/v1/teds/metadata/1

