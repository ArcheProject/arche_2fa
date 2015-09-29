 #!/bin/bash
 #You need lingua and gettext installed to run this

 echo "Updating arche_2fa.pot"
 pot-create -d arche_2fa -o arche_2fa/locale/arche_2fa.pot arche_2fa/.
 echo "Merging Swedish localisation"
 msgmerge --update  arche_2fa/locale/sv/LC_MESSAGES/arche_2fa.po  arche_2fa/locale/arche_2fa.pot
 echo "Updated locale files"
