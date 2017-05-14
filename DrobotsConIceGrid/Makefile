#!/usr/bin/make -f
# -*- mode:Makefile -*-

NODES=$(basename $(shell ls node*.config | sort -r))
IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

dir: 
	mkdir -p db
	mkdir -p db/node1
	mkdir -p db/node2
	mkdir -p db/node3
	mkdir -p db/node4
	mkdir -p db/registry

start-grid:
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! netstat -lptn 2> /dev/null | grep ":4061" > /dev/null; do \
	    sleep 1; \
	done

	@for node in $(filter-out node1, $(NODES)); do \
	    icegridnode --Ice.Config=$$node.config & \
	    echo -- $$node started; \
	done

	@echo -- ok

ice:
	$(IG_ADMIN) -e "application add 'drobots.xml'" &
	$(IG_ADMIN) -e "application update 'drobots.xml'"

all:
	make dir
	make start-grid
	make ice

ice-grid:
	make dir
	make start-grid
	make patch2calc
	icegridgui &

patch2calc:
	icepatch2calc code/

stop-grid:
	@for node in $(NODES); do \
	    $(IG_ADMIN) -e "node shutdown $$node"; \
	    echo -- $$node finished; \
	done

	@sudo killall icegridnode
	@echo -- ok

show-nodes:
	$(IG_ADMIN) -e "node list"

clean: stop-grid
	$(RM) code/*.bz2
	$(RM) code/*.sum
	sudo rm -r db/