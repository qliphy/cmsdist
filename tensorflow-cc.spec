### RPM external tensorflow-cc 1.6.0
Provides: libtensorflow_cc.so(tensorflow)(64bit)
Source: none

BuildRequires: tensorflow-sources

%prep

%build


%install

tar xfz ${TENSORFLOW_SOURCES_ROOT}/libtensorflow_cc.tar.gz -C %{i}

