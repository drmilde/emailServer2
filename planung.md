# Planung email_scheduler

Mithilfe des email_schedulers werden die ausgehenden emails verwaltet und in Abständen von 5 Minuten gesendet.

Maximal können pro Tag 240 mails geschickt werden.

Der server vewendet **apscheduler**

Bei Starten mit uvicorn muss man darauf achten, dass die app dierekt aufgerufen wird, andernfalls werden mehrere instanzen der app gestaret und entsprechend laufen mehrere Scheduler parallel 

Ein lifespan sollte genutzt werden, um den Server korrekt herunterzufahren.

