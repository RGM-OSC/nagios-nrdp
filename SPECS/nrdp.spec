%define name nrdp
%define version 1.4
%define release 2.rgm

Name               : %{name}
Version            : %{version}
Release            : %{release}
Summary            : NRDP module for Nagios
License            : BSD
URL                : https://exchange.nagios.org/directory/Addons/Passive-Checks/NRDP--2D-Nagios-Remote-Data-Processor/details
Source0            : %{name}-%{version}.tar.gz


Group              : Applications/Monitoring

BuildRoot          : %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Requires           : rgm-base nagios
Provides           : ndrp


%define datadir %{rgm_path}/%{name}-%{version}
%define linkdir %{rgm_path}/%{name}


%description
Nagios Remote Data Processor (NDRP) is a flexible data transport mechanism
and processor for Nagios. It is designed with a simple and powerful
architecture that allows for it to be easily extended and customized to
fit individual users' needs. It uses standard ports protocols
(HTTP(S) and XML) and can be implemented as a replacement for NSCA.

%prep
%setup -T -b 0 -n %{name}-%{version}


%build

%install
%{__rm} -rf %{buildroot}
cd ..
install -d -m0755 %{buildroot}%{_localstatedir}/tmp/%{name}
install -d -m0755 %{buildroot}%{datadir}
install -d -m0755 %{buildroot}%{rgm_docdir}/httpd
install -D -m 0644 %{_builddir}/%{name}-%{version}/httpd-nrdp.example.conf %{buildroot}%{rgm_docdir}/httpd/
cp -afpvr %{name}-%{version}/* %{buildroot}%{datadir}


%pre
getent group %{rgm_group} >/dev/null || groupadd -r %{rgm_group}
getent passwd %{rgm_user_nagios} >/dev/null || \
    useradd -r -g %{rgm_group} -d /home/%{rgm_user_nagios} -s /sbin/nologin \
    -c "%{rgm_user_nagios} user" %{rgm_user_nagios}
exit 0

%post
ln -sf %{datadir} %{linkdir}
cp -p %{_sysconfdir}/php.ini %{_sysconfdir}/php.ini.$(date +%Y%m%d)
sed -r -i 's/(^open_basedir.*$)/\1:\/srv\/rgm\/nrdp/' /etc/php.ini
if [ -e %{_sysconfdir}/httpd/conf.d/%{name}.conf ]; then
    rm -f %{_sysconfdir}/httpd/conf.d/%{name}.conf
fi

sed -i "s/NRDP_DEFAULT_PASSWORD/$(/usr/share/rgm/random.sh -l 32 -h)/" %{datadir}/server/config.inc.php

service httpd reload >/dev/null 2>&1

%postun
unlink %{linkdir} >/dev/null 2>&1
rm -Rf %{datadir} >/dev/null 2>&1

%preun
cp -p %{_sysconfdir}/php.ini %{_sysconfdir}/php.ini.$(date +%Y%m%d)
sed -r -i 's/:\/srv\/rgm\/nrdp//' /etc/php.ini
service httpd reload >/dev/null 2>&1

%clean
%{__rm} -rf %{buildroot}


%files
%doc %{rgm_docdir}/httpd/httpd-nrdp.example.conf
%defattr(0640,%{rgm_user_nagios},%{rgm_group},0750)
%dir %{_localstatedir}/tmp/%{name}
%dir %{datadir}
%{datadir}/INSTALL.TXT
%dir %{datadir}/clients
%attr(0750,-,-) %{datadir}/clients/send_nrdp.php
%attr(0750,-,-) %{datadir}/clients/send_nrdp.sh
%{datadir}/clients/sample.xml
%doc %{datadir}/httpd-nrdp.example.conf
%{datadir}/CHANGES.TXT
%dir %{datadir}/server
%config(noreplace) %{datadir}/server/config.inc.php
%{datadir}/server/index.php
%dir %{datadir}/server/plugins
%dir %{datadir}/server/plugins/nagioscorecmd
%{datadir}/server/plugins/nagioscorecmd/nagioscorecmd.inc.php
%dir %{datadir}/server/plugins/nagioscorepassivecheck
%{datadir}/server/plugins/nagioscorepassivecheck/nagioscorepassivecheck.inc.php
%dir %{datadir}/server/includes
%{datadir}/server/includes/constants.inc.php
%{datadir}/server/includes/utils.inc.php
%{datadir}/install-html
%{datadir}/LICENSE.TXT

%changelog
* Thu Mar 11 2021 Eric Belhomme <ebelhomme@fr.scc.com> - 1.4-2.rgm
- move httpd config file as example file in /usr/share/doc/rgm/httpd/

* Mon May 06 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 1.4-1.rgm
- use rgm-macros
- NRDP token randomizaton during post-install
- fix apache config file

* Fri Mar 01 2019 Michael Aubertin <maubertin@fr.scc.com> - 1.4-0.rgm
- Update version

* Fri Feb 22 2019 Michael Aubertin <maubertin@fr.scc.com> - 1.2-0.rgm
- Initial fork

* Mon Jul  6 2015 Guillaume ONA <contribution@eyesofnetwork.com> - 1.2-0.eon
- Build for EyesOfNetwork
