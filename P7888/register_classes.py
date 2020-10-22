from labscript_devices import register_classes



# The "register_classes" method is more flexible. It allows BLACS tabs
# and runviewer parsers to be defined in any importable file within a
# subfolder of labscript_devices. Additionally, the 'user_devices'
# configuration setting in labconfig can be used to specify a
# comma-delimited list of names of importable packages containing
# additional labscript devices. Classes using the new method can be in
# files with any name, and do not need class decorators. Instead, the
# classes should be registered by creating a file called
# 'register_classes.py', which when imported, makes calls to
# labscript_devices.register_classes() to register which BLACS tab and
# runviewer parser class belong to each device. Tab and parser classes
# must be passed to register_classes() as fully qualified names, i.e.
# "labscript_devices.submodule.ClassName", not by passing in the
# classes themselves. This ensures imports can be deferred until the
# classes are actually needed. When BLACS and runviewer look up
# classes with get_BLACS_tab() and get_runviewer_parser(),
# populate_registry() will be called in order to find all files called
# 'register_classes.py' within subfolders (at any depth) of
# labscript_devices, and they will be imported to run their code and
# hence register their classes. The "new" method does not impose any
# restrictions on code organisation within subfolders of
# labscript_devices, and so is preferable as it allows auxiliary
# utilities or resource files to live in subfolders alongside the
# device code to which they are relevant, the use of subrepositories,
# the grouping of similar devices within subfolders, and other nice
# things to have.
# Taken from https://github.com/labscript-suite/labscript-utils/blob/master/labscript_utils/device_registry/_device_registry.py

with open(r'C:\Users\Boris\labscript-suite\userlib\user_devices\P7888\_register_class_ran.txt', 'w') as fp:
	pass

register_classes(
	'P7888',
	BLACS_tab = 'user_devices.P7888.blacs_tabs.P7888Tab',
	#this tells BLACS where the gui tab is, the P7888_Tab tells blacs where the worker is.
	runviewer_parser = None,
)