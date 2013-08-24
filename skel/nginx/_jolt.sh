#!/bin/bash

mkdir $JOLTDIR/$JOLTSERVICE-$JOLTNAME
cp nginx.conf $JOLTDIR/$JOLTSERVICE-$JOLTNAME/nginx.conf.tmp
cp nginx.monit $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp

sed -e "s!__JOLTDIR__!$JOLTDIR!g" \
	-e "s!__JOLTNAME__!$JOLTNAME!g" \
	$JOLTDIR/$JOLTSERVICE-$JOLTNAME/nginx.conf.tmp > $JOLTDIR/$JOLTSERVICE-$JOLTNAME/nginx.conf

sed -e "s!__JOLTDIR__!$JOLTDIR!g" \
	-e "s!__JOLTNAME__!$JOLTNAME!g" \
	$JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp > $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit

rm $JOLTDIR/$JOLTSERVICE-$JOLTNAME/nginx.conf.tmp
rm $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp

mkdir $JOLTDIR/$JOLTSERVICE-$JOLTNAME/vhosts
mkdir $JOLTDIR/$JOLTSERVICE-$JOLTNAME/tmp
$JOLTBIN ports new $JOLTSERVICE $JOLTNAME