
PROJECT = vinil
PACKAGE = config

#--------------------------------------------------------------------------
#

all: export-data-files
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


EXPORT_DATAFILES = \
	envs.sh \


CP_F = rsync
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PACKAGE)

export-data-files::
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
        } done


# version
# $Id$

# End of file