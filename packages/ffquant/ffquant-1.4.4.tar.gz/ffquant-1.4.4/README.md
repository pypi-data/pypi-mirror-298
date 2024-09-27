# Install JupyterHub

curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin tljhadmin --version 1.0.0b1

Edit ~/.profile, add the following to the end

export PATH=/opt/tljh/user/bin/:$PATH

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

nvm install 20.17.0

nvm alias default 20.17.0

sudo -E /opt/tljh/user/bin/python3 -m pip install backtrader matplotlib dash pandas netifaces psutil ffquant numpy

sudo -E /opt/tljh/user/bin/jupyter lab build

sudo systemctl restart jupyterhub jupyter-tljhadmin

Visit http://192.168.25.144 in your browser

Log in as tljhadmin and set your password


# Let new user register with username and password
sudo tljh-config set auth.type nativeauthenticator.NativeAuthenticator

sudo tljh-config reload

BE CAREFULL!!! When this feature is enabled, the admin user has to go through the sign-up process. Username must be the same with the one used in the installation command.

Admin user authorizes user registration at http://192.168.25.144/hub/authorize


# Compile ffquant and upload to PyPi
python -m pip install setuptools wheel twine

Increase version number in setup.py

python setup.py sdist bdist_wheel

python -m twine upload dist/*

Ask Joanthan for PyPi API token.