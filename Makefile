# Makefile for source rpm: gmp
# $Id$
NAME := gmp
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
