Name:           flatpak
Version:        1.0.3
Release:        5
Summary:        Application deployment framework for desktop apps
License:        LGPLv2+
URL:            http://flatpak.org/
Source0:        https://github.com/flatpak/flatpak/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0000:      modify-automake-version.patch
Patch0001:      CVE-2021-21261-1.patch
Patch0002:      CVE-2021-21261-2.patch
Patch0003:      CVE-2021-21261-3.patch
Patch0004:      CVE-2021-21261-4.patch
Patch0005:      CVE-2021-21261-5.patch
Patch0006:      CVE-2021-21381-1.patch
Patch0007:      CVE-2021-21381-2.patch
Patch0008:      CVE-2021-21381-3.patch
Patch0009:      CVE-2019-8308.patch

BuildRequires:  pkgconfig(appstream-glib) pkgconfig(gio-unix-2.0) pkgconfig(gobject-introspection-1.0) >= 1.40.0 pkgconfig(json-glib-1.0) pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(libsoup-2.4) pkgconfig(libxml-2.0) >= 2.4 pkgconfig(ostree-1) >= 2018.7 pkgconfig(polkit-gobject-1) pkgconfig(libseccomp) pkgconfig(xau)
BuildRequires:  bison bubblewrap >= 0.2.1 docbook-dtds docbook-style-xsl gettext gpgme-devel libcap-devel systemd /usr/bin/xmlto /usr/bin/xsltproc
Requires:       ostree%{?_isa} >= 2018.7 bubblewrap >= 0.2.1 ostree-libs%{?_isa} >= 2018.7
Recommends:     /usr/bin/p11-kit xdg-desktop-portal > 0.10
Provides:       %{name}-libs = %{version}-%{release}
Obsoletes:      %{name}-libs

%description
flatpak is a system for building, distributing and running sandboxed desktop
applications on Linux. See https://wiki.gnome.org/Projects/SandboxedApps for
more information.

%package devel
Summary:        Development files for %{name}
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the pkg-config file and development headers for %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure --with-priv-mode=none \
            --with-system-bubblewrap --enable-docbook-docs $CONFIGFLAGS)
%make_build V=1
sed -i 's/idm[0-9]\{5,32\}\"/idm123456789123456\"/g' %{_builddir}/flatpak-1.0.3/doc/flatpak-docs.html

%install
%make_install
install -pm 644 NEWS README.md %{buildroot}/%{_pkgdocdir}
install -d %{buildroot}%{_localstatedir}/lib/flatpak
install -d %{buildroot}%{_sysconfdir}/flatpak/remotes.d
rm -f %{buildroot}%{_libdir}/libflatpak.la
%find_lang %{name}

%post
flatpak remote-list --system &> /dev/null || :
%ldconfig_scriptlets libs

%files -f %{name}.lang
%license COPYING
%doc %{_pkgdocdir}
%{_bindir}/flatpak
%{_bindir}/flatpak-bisect
%{_bindir}/flatpak-coredumpctl
%{_datadir}/bash-completion
%{_datadir}/dbus-1/interfaces/org.freedesktop.Flatpak.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.Flatpak.xml
%{_datadir}/dbus-1/services/org.freedesktop.Flatpak.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Flatpak.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
%{_datadir}/gdm/env.d
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.Flatpak.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.Flatpak.rules
%{_datadir}/zsh/site-functions
%{_libexecdir}/flatpak-dbus-proxy
%{_libexecdir}/flatpak-portal
%{_libexecdir}/flatpak-session-helper
%{_libexecdir}/flatpak-system-helper
%dir %{_localstatedir}/lib/flatpak
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
%{_sysconfdir}/flatpak/remotes.d
%{_sysconfdir}/profile.d/flatpak.sh
%{_unitdir}/flatpak-system-helper.service
%{_userunitdir}/flatpak-portal.service
%{_userunitdir}/flatpak-session-helper.service
%{_userunitdir}/dbus.service.d
%{_libdir}/girepository-1.0/Flatpak-1.0.typelib
%{_libdir}/libflatpak.so.*

%files devel
%{_datadir}/gir-1.0/Flatpak-1.0.gir
%{_datadir}/gtk-doc/
%{_includedir}/%{name}/
%{_libdir}/libflatpak.so
%{_libdir}/pkgconfig/%{name}.pc

%files help
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/%{name}-metadata.5*
%{_mandir}/man5/flatpak-flatpakref.5*
%{_mandir}/man5/flatpak-flatpakrepo.5*
%{_mandir}/man5/flatpak-installation.5*
%{_mandir}/man5/flatpak-remote.5*

%changelog
* Mon Apr 12 2021 wangyue <wangyue92@huawei.com> - 1.0.3-5
- Fix CVE-2019-8308

* Wed Mar 24 2021 wangxiao <wangxiao65@huawei.com> - 1.0.3-4
- Fix CVE-2021-21381

* Sun Feb 07 2021 wangxiao <wangxiao65@huawei.com> - 1.0.3-3
- Modify automake version
- Fix CVE-2021-21261

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.3-2
- Package init
