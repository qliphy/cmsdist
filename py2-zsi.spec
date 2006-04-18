### RPM external py2-zsi 1.7
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{v}.tar.gz
Requires: python

%prep 
%setup -n ZSI-%v
%build
setup.py build
%install
setup.py install --prefix=%{i}
