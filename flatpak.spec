Name:           flatpak
Version:        1.10.2
Release:        2
Summary:        Application deployment framework for desktop apps
License:        LGPLv2+
URL:            http://flatpak.org/
Source0:        https://github.com/flatpak/flatpak/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0000:      modify-automake-version.patch
Patch0002:      CVE-2021-21261-2.patch
Patch0004:      CVE-2021-21261-4.patch
Patch0005:	0001-OCI-Switch-to-pax-format-for-tar-archives.patch
Patch6000:      backport-0001-CVE-2021-41133.patch
Patch6001:      backport-0002-CVE-2021-41133.patch
Patch6002:      backport-0003-CVE-2021-41133.patch
Patch6003:      backport-0004-CVE-2021-41133.patch
Patch6004:      backport-0005-CVE-2021-41133.patch
Patch6005:      backport-0006-CVE-2021-41133.patch
Patch6006:      backport-0007-CVE-2021-41133.patch
Patch6007:      backport-0008-CVE-2021-41133.patch
Patch6008:      backport-run-Handle-unknown-syscalls-as-intended.patch
Patch6009:      backport-Fix-handling-of-syscalls-only-allowed-by-de.patch

BuildRequires:  pkgconfig(appstream-glib) pkgconfig(gio-unix-2.0) pkgconfig(gobject-introspection-1.0) >= 1.40.0 pkgconfig(json-glib-1.0) pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(libsoup-2.4) pkgconfig(libxml-2.0) >= 2.4 pkgconfig(ostree-1) >= 2020.8 pkgconfig(polkit-gobject-1) pkgconfig(libseccomp) pkgconfig(xau)
BuildRequires:  bison bubblewrap >= 0.4.0 docbook-dtds docbook-style-xsl gettext gpgme-devel libcap-devel systemd xmlto libxslt
BuildRequires:  pkgconfig(libsystemd) pkgconfig(dconf) pkgconfig(fuse) pkgconfig(gdk-pixbuf-2.0) pkgconfig(libzstd) >= 0.8.1 python3-pyparsing xdg-dbus-proxy

%{?systemd_requires}
Requires:       ostree%{?_isa} >= 2020.8 bubblewrap >= 0.4.0 ostree-libs%{?_isa} >= 2020.8
Requires:	librsvg2 xdg-dbus-proxy systemd
Recommends:     p11-kit xdg-desktop-portal > 0.10
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
 %configure --with-priv-mode=none --with-system-dbus-proxy \
            --with-system-bubblewrap --enable-docbook-docs $CONFIGFLAGS)
%make_build V=1

%install
%make_install
install -pm 644 NEWS README.md %{buildroot}/%{_pkgdocdir}
install -d %{buildroot}%{_localstatedir}/lib/flatpak
install -d %{buildroot}%{_sysconfdir}/flatpak/remotes.d
rm -f %{buildroot}%{_libdir}/libflatpak.la
rm %{buildroot}%{_systemd_system_env_generator_dir}/60-flatpak-system-only

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
%{_datadir}/dbus-1/interfaces/org.freedesktop.Flatpak.Authenticator.xml
%{_datadir}/dbus-1/services/org.freedesktop.Flatpak.service
%{_datadir}/dbus-1/services/org.flatpak.Authenticator.Oci.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Flatpak.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
%{_datadir}/fish/
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.Flatpak.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.Flatpak.rules
%{_datadir}/zsh/site-functions
%{_libexecdir}/flatpak-oci-authenticator
%{_libexecdir}/flatpak-validate-icon
%{_libexecdir}/revokefs-fuse
%{_libexecdir}/flatpak-portal
%{_libexecdir}/flatpak-session-helper
%{_libexecdir}/flatpak-system-helper
%dir %{_localstatedir}/lib/flatpak
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
%{_sysconfdir}/flatpak/remotes.d
%{_sysconfdir}/profile.d/flatpak.sh
%{_unitdir}/flatpak-system-helper.service
%{_sysusersdir}/flatpak.conf
%{_userunitdir}/flatpak-session-helper.service
%{_userunitdir}/flatpak-oci-authenticator.service
%{_userunitdir}/flatpak-portal.service
%{_systemd_user_env_generator_dir}/60-flatpak
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
* Thu Oct 21 2021 xingxing <xingxing9@huawei.com> - 1.10.2-2
- Fix CVE-2021-41133

* Tue Jun 29 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 1.10.2-1
- Upgrade to 1.10.2
- Delete patches that existed in this version 1.10.2, delete sed option
  cause no file flatpak-docs.html
- Reserve three patches that still effictive
- Add patch 0001-OCI-Switch-to-pax-format-for-tar-archives.patch

* Mon Apr 12 2021 wangyue <wangyue92@huawei.com> - 1.0.3-5
- Fix CVE-2019-8308

* Wed Mar 24 2021 wangxiao <wangxiao65@huawei.com> - 1.0.3-4
- Fix CVE-2021-21381

* Sun Feb 07 2021 wangxiao <wangxiao65@huawei.com> - 1.0.3-3
- Modify automake version
- Fix CVE-2021-21261

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.3-2
- Package init
