#!/bin/bash

PORTBT=`$JOLTBIN ports new $JOLTSERVICE ${JOLTNAME}bt`
PORTRPC=`$JOLTBIN ports new $JOLTSERVICE ${JOLTNAME}rpc`

mkdir $JOLTDIR/$JOLTSERVICE-$JOLTNAME
cp transmission.monit $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp
cp settings.json $JOLTDIR/$JOLTSERVICE-$JOLTNAME/settings.json.tmp

sed -e "s!__JOLTDIR__!$JOLTDIR!g" \
	-e "s!__JOLTNAME__!$JOLTNAME!g" \
	-e "s!__PORTBT__!$PORTBT!g" \
	-e "s!__PORTRPC__!$PORTRPC!g" \
	-e "s!__USER__!$USER!g" \
	-e "s!__HOME__!$HOME!g" \
	$JOLTDIR/$JOLTSERVICE-$JOLTNAME/settings.json.tmp > $JOLTDIR/$JOLTSERVICE-$JOLTNAME/settings.json

sed -e "s!__JOLTDIR__!$JOLTDIR!g" \
	-e "s!__JOLTNAME__!$JOLTNAME!g" \
	-e "s!__PORTBT__!$PORTBT!g" \
	-e "s!__PORTRPC__!$PORTRPC!g" \
	-e "s!__USER__!$USER!g" \
	-e "s!__HOME__!$HOME!g" \
	$JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp > $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit

echo "Password is currently set to password. To change: "
echo "   monit stop $JOLTSERVICE-$JOLTNAME"
echo "   edit rpc-password in $JOLTDIR/$JOLTSERVICE-$JOLTNAME/settings.json"
echo "   monit start $JOLTSERVICE-$JOLTNAME"

mkdir $HOME/torrents
rm $JOLTMONITD/$JOLTSERVICE-$JOLTNAME.monit.tmp
rm $JOLTDIR/$JOLTSERVICE-$JOLTNAME/settings.json.tmp

echo "The web port is ${PORTRPC}"