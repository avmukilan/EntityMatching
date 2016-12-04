from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, _escape_cdata
from xml.dom import minidom
import html2text as html2text
import lxml.etree as etree


class InstructionReaderAndXmlGenerator():

    def parseAndGenerate(self, overviewFile, outputfile, numberoftests = 10):
        attributes = self.getAttributes(overviewFile)
        questionString = self.getQuestion(overviewFile)
        datasetName = self.getDataSetName(overviewFile)

        root = Element("QuetionForm" , name="xmlns=""http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd")
        overview = SubElement(root, "Overview")
        overviewFormattedContent = SubElement(overview, "FormattedContent")
        content = ""
        with open(overviewFile) as f:
            for line1 in f:
                content = content + line1

        #print content
        overviewFormattedContent.text =  '<![CDATA[' + content.replace(']]>', ']]]]><![CDATA[>') + ']]>'

        for i in range(numberoftests):
            question = SubElement(root, "Question")
            SubElement(question, "QuestionIdentifier").text = "${instanceid{%d}}" % i
            SubElement(question, "IsRequired").text = 'true'
            questionContent = SubElement(question, "QuestionContent")

            table = Element("table" , name='cellspacing='"'4'"' cellpadding='"'2'"' border='"'1'"'')
            tbody = SubElement(table, "tbody")
            tr = SubElement(tbody,"tr")
            td = SubElement(tr,"td")
            td1 = SubElement(tr,"td").text = "${%s 1}" % datasetName
            td2 = SubElement(tr,"td").text = "${%s 1}" % datasetName
            for attribute in attributes:
                tr = SubElement(tbody,"tr")
                td = SubElement(tr,"td")
                td1 = SubElement(tr,"td").text = "${a%s0}" % attribute
                td2 = SubElement(tr,"td").text = "${b%s1}" % attribute

            formattedContent = SubElement(questionContent, "FormattedContent")

            xml = minidom.parseString(ElementTree.tostring(table)) # or xml.dom.minidom.parseString(xml_string)
            pretty_xml_as_string = xml.toprettyxml()

            h3String = "<h3>Task {0}</h3>".format(i+1)
            h4String = "<h4>{0}</h4>".format(questionString)
            formattedContentTest = "\n\t\t\t{0}\n\t\t\t{1} {2}".format(h3String, h4String, pretty_xml_as_string)
            print formattedContentTest
            formattedContent.text ='<![CDATA[' + formattedContentTest.replace(']]>', ']]]]><![CDATA[>') + ']]>'

            answerSpec = SubElement(question, "AnswerSpecification")
            selectionAns = SubElement(answerSpec, "SelectionAnswer")
            SubElement(selectionAns, "MinSelectionCount").text = '1'
            SubElement(selectionAns,"MaxSelectionCount").text = '1'
            SubElement(selectionAns,"StyleSuggestion").text = 'radiobutton'
            selections = SubElement(selectionAns, "Selections")

            selection1 = SubElement(selections, "Selection")
            SubElement(selection1,"SelectionIdentifier").text = '1'
            SubElement(selection1,"Text").text = 'Same'
            selection2 = SubElement(selections, "Selection")
            SubElement(selection2,"SelectionIdentifier").text = '0'
            SubElement(selection2,"Text").text = 'Different'
            selection3 = SubElement(selections, "Selection")
            SubElement(selection3,"SelectionIdentifier").text = '2'
            SubElement(selection3,"Text").text = 'Can not tell'

            question = SubElement(root,"Question")
            SubElement(question,"QuestionIdentifier").text = "comments"
            questionContent = SubElement(question, "QuestionContent")
            SubElement(questionContent, "Text").text = "Please help us improve this HIT by including any Questions and/or Comments (optional):"
            answerSpec = SubElement(question, "AnswerSpecification")
            freeTextAns = SubElement(answerSpec, "FreeTextAnswer")
            SubElement(freeTextAns,"NumberOfLinesSuggestion").text = '5'

            tostring = ElementTree.tostring(root)
            escape = self.escape(tostring)

            xml = minidom.parseString(ElementTree.tostring(root)) # or xml.dom.minidom.parseString(xml_string)
            pretty_xml_as_string = xml.toprettyxml()
            #print pretty_xml_as_string
            x = etree.XML(escape)
            etree_tostring = etree.tostring(x, pretty_print=True)
            self_escape = self.escape(etree_tostring)

            formattedXmlToWrite = self.escape(pretty_xml_as_string)

            output_file = open(outputfile, 'w')
            output_file.write(formattedXmlToWrite)
            output_file.close()


    def parserTheFile(self, filename):
            print self.getAttributes(filename)

    def testDataSet(self,filename):
        print self.getDataSetName(filename)

    def printRange(self, range = 10):
        print range

    def escape(self, str):
        str = str.replace("&lt;", "<")
        str = str.replace("&gt;",">")
        str = str.replace("&amp;","&")
        str = str.replace("&quot;", "\"")
        #str = str.replace("<?xml version=\"1.0\" ?>","")
        #str = str.replace("&lt;","")
        return str

    def getAttributes(self, filename):
        attributes = []
        foundStart = False
        with open(filename) as f:
            for line in f:
                if line.find("ul>") != -1:
                    if foundStart:
                        return attributes
                    else:
                        foundStart = True
                elif line.find("li>") != -1:
                    if foundStart:
                        replace = line.replace("<", ">", line.count("<"))
                        split = replace.split(">")
                        attributes.append(split[2])

    def getQuestion(self, overview):
        return 'Compare the two restaurants &nbsp;and tell us if they are the same or not'

    def getDataSetName(self, filename):
        datasetName = ''
        foundStart = False
        with open(filename) as f:
            for line in f:
                if line.find("tr>") != -1:
                    if foundStart:
                        return datasetName
                    else:
                        foundStart = True
                elif line.find("td>") != -1:
                    if foundStart:
                        replace = line.replace("<", ">", line.count("<"))
                        split = replace.split(">")
                        datasetName = split[2].split(" ")[0]



reader = InstructionReaderAndXmlGenerator()
reader.parseAndGenerate("sampledata","questionForm.xml")
#reader.testDataSet("sampledata")
#reader.printRange(20)