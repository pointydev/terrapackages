# Generated by go2rpm 1.9.0
%bcond_without check

# https://github.com/jmorganca/ollama
%global goipath         github.com/jmorganca/ollama
Version:                0.1.23

%gometa -f


%global common_description %{expand:
Get up and running with Llama 2, Mistral, and other large language models
locally.}

%global golicenses      LICENSE
%global godocs          docs examples README.md app/README.md\\\
                        llm/ext_server/README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Get up and running with Llama 2, Mistral, and other large language models locally

License:        MIT AND Apache-2.0
URL:            %{gourl}
Source:         %{gosource}
BuildRequires:  git-core

%description %{common_description}

%gopkg

%prep
%goprep
%autopatch -p1
go mod download

%build
for cmd in cmd/* ; do
  go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -s -w -extldflags '--static-pie'" -buildmode=pie -tags 'osusergo,netgo,static_build' -v -x -o %{gobuilddir}/bin/$(basename $cmd) .
  go tool buildid -w %{gobuilddir}/bin/$(basename $cmd)
done
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -s -w -extldflags '--static-pie'" -buildmode=pie -tags 'osusergo,netgo,static_build' -v -x -o %{gobuilddir}/bin/ollama .
go tool buildid -w %{gobuilddir}/bin/ollama

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc docs examples README.md app/README.md llm/ext_server/README.md
%{_bindir}/*

%gopkgfiles

%changelog
%autochangelog
