%{?_javapackages_macros:%_javapackages_macros}
Name:          gmavenplus-plugin
Version:       1.5
Release:       0
Summary:       Integrates Groovy into Maven projects
Group:         Development/Java
License:       ASL 2.0
URL:           http://groovy.github.io/GMavenPlus/
Source0:       https://github.com/groovy/GMavenPlus/archive/%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(jline:jline)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.ant:ant-antlr)
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.ant:ant-launcher)
BuildRequires: mvn(org.apache.ivy:ivy)
BuildRequires: mvn(org.apache.maven:maven-core)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.apache.maven:maven-plugin-registry)
BuildRequires: mvn(org.apache.maven:maven-project)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires: mvn(org.apache.maven.shared:file-management)
BuildRequires: mvn(org.codehaus:codehaus-parent:pom:)
#BuildRequires: mvn(org.codehaus.groovy:groovy-all)
#BuildRequires: mvn(org.codehaus.groovy:groovy-ant)
BuildRequires: mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires: mvn(org.codehaus.plexus:plexus-cli)
BuildRequires: mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires: mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires: mvn(org.fusesource.jansi:jansi)
BuildRequires: mvn(org.mockito:mockito-all)
# IT tests deps
BuildRequires: mvn(ch.qos.logback:logback-classic)
BuildRequires: mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires: mvn(org.codehaus.plexus:plexus-utils)

BuildArch:     noarch

%description
GMavenPlus is a rewrite of GMaven, a Maven plugin
that allows you to integrate Groovy into your
Maven projects.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n GMavenPlus-%{version}

%pom_remove_plugin :maven-clean-plugin
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-help-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-site-plugin

%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

# Mockito cannot mock this class: class org.codehaus.gmavenplus.mojo.AbstractGroovyMojoTest$TestGroovyMojo
rm -r src/test/java/org/codehaus/gmavenplus/mojo/AbstractGroovyMojoTest.java

# Convert from dos to unix line ending
sed -i.orig 's|\r||g' README.markdown
touch -r README.markdown.orig README.markdown
rm README.markdown.orig

%mvn_file : %{name}

%build

%mvn_build -- -Pnonindy

%install
%mvn_install

%files -f .mfiles
%doc README.markdown
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 01 2015 gil cattaneo <puntogil@libero.it> 1.5-1
- initial rpm
