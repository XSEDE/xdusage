#!/usr/bin/perl

use Getopt::Long;
use Pod::Usage;
use File::Copy;
use strict;
use warnings;

my $username = "";
my $instdir = "";
my $help = 0;

my $result = GetOptions ("username=s"	=> \$username,
		      "dir=s"		=> \$instdir,
		      "help|?"		=> \$help);
pod2usage(1) if $help;

eval "require Getopt::Long; 1" or die "you need Getopt::Long to use xdusage";
eval "require Date::Manip; 1" or die "you need Date::Manip to use xdusage";
eval "require DBD::Pg; 1" or die "you need DBD::Pg (compiled w/ SSL) to use xdusage";

if (!$username){
    print "Please choose the (non-root) user to run xdusage: ";
    chomp ($username = <>);
}
if (!$instdir){
    print "Please choose the install directory: ";
    chomp ($instdir = <>);
}

unless(-e $instdir or mkdir $instdir) {
	die "Unable to create $instdir\n";
}
print "$instdir/xdusage\n";
my $file = "$instdir/xdusage";
open (WRAPPERFILE, '>', $file) or die "couldn't open: $!";
print WRAPPERFILE "#!/bin/bash\nRUNAS=\'$username\'\nXDUSAGE_INSTALL_DIR=\'$instdir\'\nexport XDUSAGE_INSTALL_DIR \n#echo \$XDUSAGE_INSTALL_DIR \nRUNCMD=\"\${XDUSAGE_INSTALL_DIR}/xdusage.pl\"\n/usr/bin/sudo -u \${RUNAS} USER=\${USER} XDUSAGE_INSTALL_DIR=\${XDUSAGE_INSTALL_DIR} \${RUNCMD} \$*\n";
close WRAPPERFILE;
chmod 0755, $file or die "Couldn't chmod $file: $!";

$file = "$instdir/xdusage.modules";
open (SAMPLEMODULE, '>', $file) or die "couldn't open: $!";
print SAMPLEMODULE "#%Module\n";
print SAMPLEMODULE "# \$Copyright\n";
print SAMPLEMODULE "##** Copyright © 2013 Pittsburgh Supercomputing Center (PSC).\n";
print SAMPLEMODULE "##**\n";
print SAMPLEMODULE "##** Permission to use, copy, and modify this software and its documentation\n";
print SAMPLEMODULE "##** without fee for personal use or non-commercial use within your\n";
print SAMPLEMODULE "##** organization is hereby granted, provided that the above copyright notice\n";
print SAMPLEMODULE "##** is preserved in all copies and that the copyright and this permission\n";
print SAMPLEMODULE "##** notice appear in supporting documentation.  Permission to redistribute\n";
print SAMPLEMODULE "##** this software to other organizations or individuals is not permitted\n";
print SAMPLEMODULE "##** without the written permission of the Pittsburgh Supercomputing\n";
print SAMPLEMODULE "##** Center.  PSC makes no representations about the suitability of this\n";
print SAMPLEMODULE "##** software for any purpose. It is provided \"as is\" without expressed nor\n";
print SAMPLEMODULE "##** implied warranty.\n";
print SAMPLEMODULE "# \$\n\n";
print SAMPLEMODULE "# Module xdusage/1.0-r6\n\n";
print SAMPLEMODULE "set description \"adds XSEDE xdusage tool to paths in the login shell environment\"\n\n";
print SAMPLEMODULE "set version 1.0-r6\n\n";
print SAMPLEMODULE "proc ModulesHelp { } {\n";
print SAMPLEMODULE "   global description\n";
print SAMPLEMODULE "   puts stderr \"\\txdusage/\$version \$description\"\n";
print SAMPLEMODULE "}\n\n";
print SAMPLEMODULE "module-whatis  \$description\n\n";
print SAMPLEMODULE "set xdusage_instdir $instdir\n\n";
print SAMPLEMODULE "remove-path    PATH   \$xdusage_instdir\n";
print SAMPLEMODULE "prepend-path   PATH   \$xdusage_instdir\n\n";
print SAMPLEMODULE "setenv         XDUSAGE_INSTALL_DIR   \$xdusage_instdir\n";
close (SAMPLEMODULE);

#system (cp xdusage.pl $instdir);
my $instfile="$instdir/xdusage.pl";
copy ("xdusage.pl", $instfile) or die "Couldn't copy xdusage.pl\n";
copy ("../docs/xdusage.1", $instdir) or die "Couldn't copy xdusage.1\n";
chmod 0700, $instfile or die "Couldn't chmod $instfile: $!";

#Create resource_name
     print "Please create: $instdir/resource_name\n";
     print "It should contain the resource name used by the XDCDB for your resource.\n";




__END__

=head 1 xdusage install

xdusageinst [options]

  Options:
    -help	brief help message
    -user	username to run xdusage as (non-root)
    -dir	installation directory into which to put xdusage

=cut
