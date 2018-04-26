%define strip /bin/true
%define __requires_exclude  ^.*$
%define __find_requires     %{nil}
%global debug_package       %{nil}
%define __provides_exclude_from ^.*$

%define _target_cpu %{device_rpm_architecture_string}

Name:          droidmedia
Summary:       Android media wrapper library
Version:       0.20170214.0
Release:       1
Group:         System/Libraries
License:       ASL 2.0
BuildRequires: ubu-trusty
BuildRequires: sudo-for-abuild
BuildRequires: droid-bin-src-full
Source0:       %{name}-%{version}.tgz
AutoReqProv:   no

%description
%{summary}

%package       devel
Summary:       droidmedia development headers
Requires:      droidmedia = %{version}-%{release}
BuildArch:     noarch

%description   devel
%{summary}

%prep

%if %{?device_rpm_architecture_string:0}%{!?device_rpm_architecture_string:1}
echo "device_rpm_architecture_string is not defined"
exit -1
%endif

%setup -T -c -n droidmedia
sudo chown -R abuild:abuild /home/abuild/src/droid/
mv /home/abuild/src/droid/* .
mkdir -p external
pushd external
tar -zxf %SOURCE0
mv droidmedia* droidmedia
popd

cat /dev/null > external/droidmedia/env.mk

%if %{?force_hal:1}%{!?force_hal:0}
echo Forcing Camera HAL connect version %{force_hal}
echo FORCE_HAL := %{force_hal} >> external/droidmedia/env.mk
%endif

%build

%define defined yep

echo test1
if (grep -qi 'something.that.doesnt.exist' device/*/*/*.mk) || %{?undefined:1}%{!?undefined:0}; then
echo cond1 = false, cond2 = false, we should never see this
fi
echo test2
if (grep -qi 'a' device/*/*/*.mk) || %{?undefined1:1}%{!?undefined1:0}; then
echo cond1 = true, cond2 = false, we should always see this
fi
echo test3
if (grep -qi 'something.that.doesnt.exist' device/*/*/*.mk) || %{?defined:1}%{!?defined:0}; then
echo cond1 = false, cond2 = true, we should always see this
fi
echo test4
if (grep -qi 'a' device/*/*/*.mk) || %{?defined:1}%{!?defined:0}; then
echo cond1 = true, cond2 = true, we should always see this
fi
echo test5
if (grep -qi 'something.that.doesnt.exist' device/*/*/*.mk) || %{?droidmedia_32bit:1}%{!?droidmedia_32bit:0}; then
echo cond1 = false, cond2 = depends, we should only see this, when droidmedia_32bit is defined
fi
echo test6
if (grep -qi 'a' device/*/*/*.mk) || %{?droidmedia_32bit:1}%{!?droidmedia_32bit:0}; then
echo cond1 = true, cond2 = depends, we should always see this
fi

if (grep -qi '^BOARD_QTI_CAMERA_32BIT_ONLY := true' device/*/*/*.mk) || %{?droidmedia_32bit:1}%{!?droidmedia_32bit:0}; then
echo DROIDMEDIA_32 := true >> external/droidmedia/env.mk
droid-make %{?_smp_mflags} libdroidmedia_32 minimediaservice minisfservice libminisf_32
else
droid-make %{?_smp_mflags} libdroidmedia minimediaservice minisfservice libminisf
fi

%install

mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/lib/
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/bin/
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/droidmedia/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/droidmedia/

cp out/target/product/*/system/lib/libdroidmedia.so \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/lib/

cp out/target/product/*/system/lib/libminisf.so \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/lib/

cp out/target/product/*/system/bin/minimediaservice \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/bin/

cp out/target/product/*/system/bin/minisfservice \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/bin/

cp external/droidmedia/*.h $RPM_BUILD_ROOT/%{_includedir}/droidmedia/
cp external/droidmedia/hybris.c $RPM_BUILD_ROOT/%{_datadir}/droidmedia/

%files
%defattr(-,root,root,-)
%{_libexecdir}/droid-hybris/system/lib/libdroidmedia.so
%{_libexecdir}/droid-hybris/system/lib/libminisf.so
%{_libexecdir}/droid-hybris/system/bin/minimediaservice
%{_libexecdir}/droid-hybris/system/bin/minisfservice

%files devel
%defattr(-,root,root,-)
%{_includedir}/droidmedia/*.h
%{_datadir}/droidmedia/hybris.c
