# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
"""
Unit tests for the following classes (modules):
    Namelist, Card, QEParser, QEInput
"""

import unittest
import fixtures
from namelist import Namelist
from card import Card
from qeparser import QEParser
from qeinput import QEInput
from filter import Filter

class QEParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    # Namelist tests
    def test_namelist_name(self):
        nl  = Namelist("Control")
        self.assertEqual(nl.name(), "control")
        nl.setName("SyStem")
        self.assertEqual(nl.name(), "system")


    def test_namelist_set_get(self):
        nl  = Namelist("control")
        self.assertEqual(nl.get("title"), None)
        
        nl.set("title", "hello")
        self.assertEqual(nl.get("title"), "hello")
        self.assertEqual(nl.get("title", quotes=True), "hello") # should not add quotes
        
        nl.set("Title", "'hello'")
        self.assertEqual(nl.get("titlE", quotes=False), "hello")
        self.assertEqual(nl.get("title"), "'hello'")


    def test_namelist_remove_exists(self):
        nl  = Namelist("control")
        nl.set("title", "hello")
        self.assertEqual(nl.exists("title"), True)
        self.assertEqual(nl.exists("Title"), True)

        nl.remove("title")
        self.assertEqual(nl.exists("title"), False)


    def test_namelist_tostring(self):
        nl  = Namelist("control")
        nl.set("title", "hello")
        self.assertEqual(nl.toString(), fixtures.assertNL)
        self.assertEqual(nl.toString(indent=3), fixtures.assertNL_space_3)


    # Card tests
    def test_card_arg(self):
        c   = Card("atomic_positions")
        self.assertEqual(c.arg(), None)

        c.setArg("alat")
        self.assertEqual(c.arg(), "alat")


    def test_card_lines(self):
        c   = Card("atomic_positions")
        c.addLine(" Ni 0.00 0.00 0.00 ")
        self.assertEqual(c.line(0), "Ni 0.00 0.00 0.00")    # should strip side spaces

        c.addLine(" Ni 0.50 0.50 0.50 ")
        self.assertEqual(len(c.lines()), 2)


    def test_card_remove_lines(self):
        c   = Card("atomic_positions")
        c.addLine(" Ni 0.00 0.00 0.00 ")
        c.addLine(" Ni 0.50 0.50 0.50 ")
        c.removeLine(0)
        self.assertEqual(c.line(0), "Ni 0.50 0.50 0.50")

        c.editLines(["a", "b"])
        self.assertEqual(c.lines(), ["a", "b"])


    def test_card_tostring(self):
        c   = Card("atomic_positions")
        c.addLine(" Ni 0.00 0.00 0.00 ")
        self.assertEqual(c.toString(), fixtures.assertC_no_arg)

        c.setArg("alat")
        self.assertEqual(c.toString(indent=3), fixtures.assertC_arg)


    # QEParse tests
    def test_qeparser_matdyn(self):
        # Attachment after card
        parser    = QEParser(configText = fixtures.textMatdyn, type="matdyn")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertMatdyn)


    def test_qeparser_dynmat(self):
        # Slash and name of namelist on the same line with parameters
        parser    = QEParser(configText = fixtures.textDynmat, type="dynmat")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertDynmat)


    def test_qeparser_file(self):
        # Configuration file
        parser    = QEParser(filename = "ni.scf.in")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertFile)


    def test_qeparser_card(self):
        # Card
        parser    = QEParser(configText = fixtures.textCards)
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertCards)


    def test_qeparser_comma(self):
        # Parameters on the same line separated by comma - does not parse as it
        # should (intentionally)
        parser          = QEParser(configText = fixtures.textComma, type="matdyn")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertComma)


    def test_qeparser_header(self):
        # Header for PH configuration files is mandatory
        parser          = QEParser(configText = fixtures.textHeader, type="ph")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertHeader)


    def test_qeparser_type(self):
        # Type of configuration file recognizes specific namelists and card only!
        parser          = QEParser(configText = fixtures.textHeader, type="pw")
        parser.parse()
        self.assertEqual(parser.toString(), '') # namelist 'INPUTPH' is not recognized


    def test_qeparser_comments(self):
        # Filters out comments
        parser          = QEParser(filename = "ph.mgb2.in", type="ph")
        parser.parse()
        self.assertEqual(parser.toString(), fixtures.assertMgB2)


    # QEInput tests
    def test_qeinput_namelist(self):
        input       = QEInput(config=fixtures.textMain)
        input.parse()
        # If non-standard card is requested, it will not add it!
        nl          = input.namelist("SOME_NAMELIST")
        self.assertEqual(input.namelistExists("some_namelist"), False)

        nl          = input.namelist("cell")
        self.assertEqual(input.namelistExists("cell"), True)


    def test_qeinput_card(self):
        input       = QEInput(config=fixtures.textMain)
        input.parse()
        # If non-standard card is requested, it will not add it!
        card        = input.card("SOME_CARD")
        self.assertEqual(input.cardExists("some_card"), False)

        card        = input.card("occupations")
        self.assertEqual(input.cardExists("occupations"), True)
        
#
#
#    def test_qeinput_attach(self):
#        self.assertFalse(True)
#
#
#    def test_qeinput_parser(self):
#        self.assertFalse(True)
#
#
#    def test_qeinput_filter(self):
#        self.assertFalse(True)
#
#
#    def test_qeinput_structure(self):
#        self.assertFalse(True)


    # Filter tests
    def test_filter_name(self):
        f  = Filter("filter")
        self.assertEqual(f.name(), "filter")


    def test_filter_card(self):
        f       = Filter("filter")
        card    = {"name":      "k_points",
                   "lines":     ("4 4 4 1 1 1",),
                   "arg":       "automatic"}
        f.setCard(card)
        self.assertEqual(len(f.cards()), 1)

        cardF   = {"a": "b"}        # Doesn't have "name" key
        self.assertRaises(KeyError, f.setCard, cardF) # Exception, callable, parameters
        self.assertEqual(len(f.cards()), 1)     # Doesn't add card

        cardF2  = "simple string"
        self.assertRaises(TypeError, f.setCard, cardF2) # Exception, callable, parameters
        self.assertEqual(len(f.cards()), 1)     # Doesn't add card

        card    = f.cards()[0]      # Check values
        self.assertEqual(card.arg(), "automatic")
        self.assertEqual(card.name(), "k_points")
        self.assertEqual(card.toString(), fixtures.assertC_filter_card)

        f.removeCard("k_points")    # Remove card
        self.assertEqual(len(f.cards()), 0)


    def test_filter_namelist(self):
        f       = Filter("filter")
        nldict  = {"name":      "control",
                   "params":    {"calculation": "'scf'",
                                 "restart_mode": "'from_scratch'"}}
        f.setNamelist(nldict)
        self.assertEqual(len(f.namelists()), 1)

        nldictF     = {"a": "b"}        # Doesn't have "name" key
        self.assertRaises(KeyError, f.setNamelist, nldictF) # Exception, callable, parameters
        self.assertEqual(len(f.namelists()), 1)     # Doesn't add namelist

        nldictF2    = "simple string"
        self.assertRaises(TypeError, f.setNamelist, nldictF2) # Exception, callable, parameters
        self.assertEqual(len(f.namelists()), 1)     # Doesn't add namelist

        nl      = f.namelists()[0]      # Check values
        self.assertEqual(nl.get("calculation", quotes=False), "scf")
        self.assertEqual(nl.name(), "control")
        self.assertEqual(nl.toString(), fixtures.assertC_filter_namelist)

        f.removeNamelist("control")    # Remove namelist
        self.assertEqual(len(f.namelists()), 0)


    def test_filter_namelist(self):
        f       = Filter("filter")
        nldict  = {"name":      "control",
                   "params":    {"calculation": "'scf'",
                                 "restart_mode": "'from_scratch'"}}
        f.setNamelist(nldict)
        f.setParam("control", "tprnfor", ".true.")  # Set parameter for existing namelist
        nlA      = f.namelists()[0]
        self.assertEqual(nlA.get("tprnfor"), ".true.")

        f.setParam("system", "ibrav", "2")  # Set parameter for non-existing namelist
        self.assertEqual(len(f.namelists()), 2)
        nlB      = f.namelists()[1]
        self.assertEqual(nlB.get("ibrav"), "2")

        self.assertEqual(nlA.exists("calculation"), True)   # Before removing
        f.removeParam("control", "calculation")
        self.assertEqual(nlA.exists("calculation"), False)  # After removing


    def test_filter_apply(self):
        input   = QEInput(config=fixtures.textMain)
        input.parse()   # Place to constructor
        # Filter that adds parameters to input
        fp       = Filter("fPlus")
        fp.setParam("control", "prefix", "'ni'")
        fp.setParam("control", "pseudo_dir", "''")
        fp.setParam("control", "outdir", "''")
        fp.setCard({"name": "occupations", "lines": ("New line",)})     # Add new card
        fp.setNamelist({"name": "cell", "params": {"hello": "world"}})  # Add new namelist
        fp.setNamelist({"name": "phonon"})
        fp.apply(input, "plus")

        self.assertEqual(input.toString(), fixtures.assertPlus)

        # Filter that removes parameters from input
        fm      = Filter("fMinus")
        fm.setCard({"name": "atomic_species"})
        fm.setNamelist({"name": "phonon"})    # Remove namelist
        fm.setParam("cell", "hello")        # Remove parameter that makes namelist empty
        fm.setParam("control", "prefix")    # Remove parameter
        fm.apply(input, "minus")
        self.assertEqual(input.toString(), fixtures.assertMinus)


if __name__ == '__main__':
    unittest.main()
    


#
## !!! FINISH
#
## Tests
#def testCreateConfig():
#    print "Testing creation of config file"
#    qe  = QEInput()
#    nl  = Namelist('control')
#    nl.add('title', "'Ni'")
#    nl.add('restart_mode', "'from_scratch'")
#    print "Adding parameters to namelist:\n%s" % nl.toString()
#    nl.set('title', "'Fe'")
#    qe.addNamelist(nl)
#    print "Adding namelist to QEInput:\n%s" % qe.toString()
#
#    c = Card('atomic_species')
#    c.addLine('Ni  26.98  Ni.pbe-nd-rrkjus.UPF')
#    print "Adding line to card:\n%s" % c.toString()
#    qe.addCard(c)
#    print "Adding card to QEInput:\n%s" % qe.toString()
#    #qe.save()
#
#
#def testParseConfig():
#    print "Testing parsing config file"
#    qe  = QEInput("../tests/ni.scf.in")
#    qe.parse()
#    print qe.toString()
#    nl  = qe.namelist('control')
#    nl.add('title', 'Ni')
#    nl.remove('restart_mode')
#    qe.removeCard('atomic_species')
#    nl.set('calculation', "'nscf'")
#    c = qe.card('atomic_positions')
#    c.editLines(['Say Hi! :)'])
#    print qe.toString()
#    #qe.save("../tests/ni.scf.in.mod")
#
#def testAttach():
#    qe  = QEInput("../tests/si.ph.in", type="ph")
#    qe.parse()
#    qe.save("../tests/si.ph.in.mod")
#
#
#if __name__ == "__main__":
#    #testCreateConfig()
#    #testParseConfig()
#    testAttach()

__date__ = "$Jul 28, 2010 2:32:23 PM$"


