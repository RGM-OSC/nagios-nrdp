Name: nrdp
Version: 1.4
Release            : 0.rgm
Summary            : NRDP module for Nagios
License            : BSD
URL                : https://exchange.nagios.org/directory/Addons/Passive-Checks/NRDP--2D-Nagios-Remote-Data-Processor/details
Source0            : %{name}-%{version}.tar.gz


Group              : Applications/Monitoring

BuildRoot          : %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Requires           : nagios
Provides           : ndrp


%define rgmdir /srv/rgm
%define datadir %{rgmdir}/%{name}-%{version}
%define linkdir %{rgmdir}/%{name}
%define appuser nagios
%define appgroup rgm

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
cp -afpvr %{name}-%{version}/* %{buildroot}%{datadir}
install -D -m 0644 %{name}-%{version}/%{name}.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf

%pre
getent group %{appgroup} >/dev/null || groupadd -r %{appgroup}
getent passwd %{appuser} >/dev/null || \
    useradd -r -g %{appgroup} -d /home/%{appuser} -s /sbin/nologin \
    -c "%{appuser} user" %{appuser}
exit 0

%post
ln -sf %{datadir} %{linkdir}
cp -p %{_sysconfdir}/httpd/conf/httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf.$(date +%Y%m%d)
sed -i -r 's/(^Include conf.d\/thruk.conf)/\1\nInclude conf.d\/nrdp.conf\n/' %{_sysconfdir}/httpd/conf/httpd.conf
cp -p %{_sysconfdir}/php.ini %{_sysconfdir}/php.ini.$(date +%Y%m%d)
sed -r -i 's/(^open_basedir.*$)/\1:\/srv\/rgm\/nrdp/' /etc/php.ini
service httpd reload >/dev/null 2>&1

%postun
unlink %{linkdir} >/dev/null 2>&1
rm -Rf %{datadir} >/dev/null 2>&1

%preun
cp -p %{_sysconfdir}/httpd/conf/httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf.$(date +%Y%m%d)
sed -i -r 's/^Include conf\.d\/nrdp\.conf$//' /etc/httpd/conf/httpd.conf
cp -p %{_sysconfdir}/php.ini %{_sysconfdir}/php.ini.$(date +%Y%m%d)
sed -r -i 's/:\/srv\/rgm\/nrdp//' /etc/php.ini
service httpd reload >/dev/null 2>&1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0640,%{appuser},%{appgroup},0750)
%dir %{_localstatedir}/tmp/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{datadir}
%{datadir}/INSTALL.TXT
%dir %{datadir}/clients
%attr(0750,-,-) %{datadir}/clients/send_nrdp.php
%attr(0750,-,-) %{datadir}/clients/send_nrdp.sh
%{datadir}/clients/sample.xml
%{datadir}/nrdp.conf
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
* Fri Feb 22 2019 Michael Aubertin <maubertin@fr.scc.com> - 1.2-0.rgm
- Initial fork
* Mon Jul  6 2015 Guillaume ONA <contribution@eyesofnetwork.com> - 1.2-0.eon 
- Build for EyesOfNetwork
