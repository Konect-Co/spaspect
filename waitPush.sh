inotifywait -r -m -e close_write ./firebaseFiles | while read events
do
	cd firebaseScripts
	node pushFirebase.js
done
