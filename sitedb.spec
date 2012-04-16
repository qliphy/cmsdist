### RPM cms sitedb 2.3.1
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES
## INITENV SETV SITEDB_LEGACY_PYTHONPATH %i/legacy


%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define cvssrc cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
#%define svnsrc svn://svn.cern.ch/reps/CMSDMWM/SiteDB/trunk@15167
%define svnsrc svn://svn.cern.ch/reps/CMSDMWM/SiteDB/tags/%{realversion}
Source0: https://github.com/lat/WMCore/zipball/cdea8357c116e32e7229af7f4ff322e72f6e6643#/wmcore_sitedb.zip
Source1: %{svnsrc}?scheme=svn+ssh&strategy=export&module=SiteDB&output=/sitedb.tar.gz
#Source1: https://cern.ch/lat/temp/sitedb5.tar.gz
Source2: %{cvssrc}&strategy=export&module=WEBTOOLS&nocache=true&export=WEBTOOLS&tag=-rSiteDBv1-slc5-v3&output=/old-sitedb.tar.gz
Source3: %{cvssrc}&strategy=export&module=WEBTOOLS&nocache=true&export=WEBTOOLS&tag=-rV01-03-47&output=/old-webtools.tar.gz
Requires: cherrypy yui3 d3 xregexp py2-cx-oracle py2-cjson py2-pycurl rotatelogs wmcore-devtools
Requires: yui py2-cheetah py2-pysqlite py2-formencode py2-pycrypto beautifulsoup py2-sqlalchemy oracle-env py2-pyopenssl
# ^ = line for legacy SiteDB support, remove when migrating fully to sitedb 2.x
#BuildRequires: wmcore-devtools

%prep
%setup -T -b 0 -n lat-WMCore-cdea835
%setup -D -T -b 1 -n SiteDB
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/conf.py
%setup -D -T -c -a 2 -n LEGACY-SITEDB
rm -f WEBTOOLS/Applications/SiteDB/Utilities/MigrateSites # requires phedex
rm -f WEBTOOLS/Applications/SiteDB/Schema/writergrants.py
%setup -D -T -c -a 3 -n LEGACY-WEBTOOLS
rm -rf WEBTOOLS/{Applications,Configuration,Tools/StartupScripts}
rm -fr WEBTOOLS/SecurityModule/{perl,crypttest}

%build
cd ../*WMCore*
python setup.py build_system -s wmc-rest
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../SiteDB
python setup.py build_system --compress

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../*WMCore*
python setup.py install_system -s wmc-rest --prefix=%i
cd ../SiteDB
python setup.py install_system --compress --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

cd ../LEGACY-WEBTOOLS/WEBTOOLS
mkdir -p %i/legacy
cp -r * %i/legacy
cp cmsWeb %i/bin

cd ../../LEGACY-SITEDB/WEBTOOLS
mkdir -p %i/legacy/Applications
cp -r Applications/SiteDB %i/legacy/Applications
mkdir -p %i/legacy/Applications/SiteDB/csv

python -m compileall %i/legacy || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export YUI3_ROOT D3_ROOT XREGEXP_ROOT SITEDB_ROOT SITEDB_VERSION;") > %i/etc/profile.d/env.sh

%post
%{relocateConfig}etc/profile.d/{env,dep*}.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
