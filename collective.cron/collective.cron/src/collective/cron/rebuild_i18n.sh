#!/usr/bin/env bash
PRODUCTNAME='collective.cron'
I18NDOMAIN=$PRODUCTNAME
i18ndude=$(which i18ndude)
CWD=$(dirname $0)
cd ${CWD}
echo "Using ${i18ndude} in ${CWD}"
# Synchronise the .pot with the templates.
${i18ndude} rebuild-pot --pot locales/${PRODUCTNAME}.pot --merge locales/${PRODUCTNAME}-manual.pot --create ${I18NDOMAIN} .
# Synchronise the resulting .pot with the .po files
for po in locales/*/LC_MESSAGES/${PRODUCTNAME}.po;do 
    ${i18ndude} sync --pot locales/${PRODUCTNAME}.pot $po
done
