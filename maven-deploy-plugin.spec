%global pkg_name maven-deploy-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.7
Release:        11.12%{?dist}
Summary:        Maven Deploy Plugin

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-deploy-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

BuildArch: noarch

# Basic stuff
BuildRequires: %{?scl_prefix_java_common}javapackages-tools

# Maven and its dependencies
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: maven30-maven-plugin-plugin
BuildRequires: maven30-maven-resources-plugin
BuildRequires: maven30-maven-archiver
BuildRequires: maven30-mvn(org.apache.maven:maven-artifact:2.0.6)
BuildRequires: maven30-mvn(org.apache.maven:maven-model:2.0.6)
# The following maven packages haven't updated yet
BuildRequires: maven30-maven-changes-plugin
BuildRequires: maven30-maven-enforcer-plugin
BuildRequires: maven30-maven-invoker-plugin

# autorequires support for compat packages not finished yet
Requires: maven30-mvn(org.apache.maven:maven-artifact:2.0.6)
Requires: maven30-mvn(org.apache.maven:maven-model:2.0.6)

%description
Uploads the project artifacts to the internal remote repository.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x

%pom_xpath_inject pom:project "<build><plugins/></build>"
%pom_add_plugin :maven-plugin-plugin . "
        <configuration>
          <helpPackageName>org.apache.maven.plugin.deploy</helpPackageName>
        </configuration>"
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
# A test class doesn't compile
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc DEPENDENCIES LICENSE NOTICE
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.7-11.12
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.7-11.10
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.7-11.9
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.8
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.7
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.6
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.5
- Remove requires on java

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-11.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.7-11
- Mass rebuild 2013-12-27

* Mon Aug 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.7-10
- Migrate away from mvn-rpmbuild (#997454)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-8
- Remove unneeded BR: maven-idea-plugin

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-7
- Drop patch for maven-compat
- Add missing requires on maven2 artifact and model
- Explictly set helpPackageName in maven-plugin-plugin configuration
- Resolves: rhbz#914167

* Tue Feb 26 2013 Weinan Li <weli@redhat.com> - 2.7-6
- bz915609
- Remove doxia dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.7-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Tomas Radej <tradej@redhat.com> - 2.7-1
- Update to upstream 2.7
- Guidelines fixes

* Tue May 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.6-1
- Update to upstream 2.6.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Weinan Li <weli@redhat.com> - 0:2.5-5
- skip test during building

* Wed Jun 2 2010 Weinan Li <weli@redhat.com> - 0:2.5-4
- remove the Epoch section

* Wed Jun 2 2010 Weinan Li <weli@redhat.com> - 0:2.5-3
- Fix URL
- Add Epoch

* Wed Jun 2 2010 Weinan Li <weli@redhat.com> - 2.5-2
- depmap removed
- Use new BRs for some already updated maven components
- obsolete/provide maven2-plugin-deploy
- Remove the empty line between changelog and the changelog entry

* Mon May 31 2010 Weinan Li <weli@redhat.com> - 2.5-1
- Initial Package
