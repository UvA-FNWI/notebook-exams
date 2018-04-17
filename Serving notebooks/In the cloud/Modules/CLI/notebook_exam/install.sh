#!/bin/sh

ret=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
if [ $ret -eq 0 ]; then
    echo "notebook-exam requires Python 2.7."
    exit
fi

echo "Installing notebook-exam module..."
pip uninstall -y notebook-exam 1> /dev/null
pip install https://github.com/jessesar/notebook-exam-cli/archive/master.zip 1> /dev/null

echo "Installing questions module (Python 2.7)..."
pip uninstall -y questions 1> /dev/null
pip install https://github.com/jessesar/uva-questions/archive/master.zip 1> /dev/null

if hash pip3 2>/dev/null; then
    echo "Installing questions module (Python 3)..."
    pip3 uninstall -y questions 1> /dev/null
    pip3 install https://github.com/jessesar/uva-questions/archive/master.zip 1> /dev/null
fi

if [ -f ~/anaconda/envs/python3/bin/pip ]; then
    echo "Installing questions module (Python 3)..."
    ~/anaconda/envs/python3/bin/pip uninstall -y questions 1> /dev/null
    ~/anaconda/envs/python3/bin/pip install https://github.com/jessesar/uva-questions/archive/master.zip 1> /dev/null
fi

echo "Enabling Jupyter Widgets..."

jupyter nbextension enable --py widgetsnbextension

bold=$(tput bold)
normal=$(tput sgr0)

echo ""
echo " ---------------- "
echo "| NOTEBOOK EXAMS |"
echo " ---------------- "
echo ""
echo "The ${bold}notebook-exam${normal} command has been installed."

if [ -f ~/.notebook-exam-password ]; then
    echo "Existing login credentials were found. You can now use '${bold}notebook-exam${normal}'."
else
    echo "Please authenticate first using '${bold}notebook-exam authenticate YOUR_PASSWORD${normal}'."
fi

echo ""
echo "For further reference, please run 'notebook-exam --help'."
echo ""