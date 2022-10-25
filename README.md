# script.LibreTranslate
Kodi addon to integrate with LibreTranslate to be able to translate on the fly

Update: V 0.0.8 :
- Use Simplecache to store lookups for 30 days, to process faster for already translated text


Update: V 0.0.7 :
- Added ability to send parameters to allow multiple calls and specify where to store results.

for example, can call twice in a skin:

<onload>RunScript(script.LibreTranslate,q=hola,property=a)</onload>
<onload>RunScript(script.LibreTranslate,q=adiós,property=b)</onload>

q=hola and q=adiós are static text strings, but could use $INFO[] like:

<onload>RunScript(script.LibreTranslate,q=$INFO[ListItem.Label]),property=a)</onload>
<onload>RunScript(script.LibreTranslate,q=$INFO[ListItem.Genre]),property=b)</onload>

After calling those, you can access the results using the "property" identifier sent in the RunScript via property name that always starts with "libreTranslate_" followed by the "property" you sent (a and b in example above):

$INFO[Window(Home).Property(libreTranslate_a)]

$INFO[Window(Home).Property(libreTranslate_b)]
