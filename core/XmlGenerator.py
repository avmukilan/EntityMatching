from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, _escape_cdata
from xml.dom import minidom

root = Element("QuetionForm" , name="xmlns=""http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd")
overview = SubElement(root, "Overview")

output_file = open( 'questionForm.xml', 'w')

attributes = ['Name', 'Address', 'City', 'Phone', 'Email']
datasetName = 'Restuarant'
questionString = 'Compare the two restaurants &nbsp; and tell us if they are the same or not'

def escape( str ):
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;",">")
    str = str.replace("&amp;","&")
    str = str.replace("&quot;", "\"")
    #str = str.replace("<?xml version=\"1.0\" ?>","")
    #str = str.replace("&lt;","")
    return str

for i in range(10):
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

    data = ElementTree.tostring(table)
    h3 = Element("h3")
    h3.text = "Task %d" % ( i + 1)
    h4 = Element("h4")
    h4.text = "{0}".format(questionString)

    xml = minidom.parseString(ElementTree.tostring(h3)) # or xml.dom.minidom.parseString(xml_string)
    h3_String = xml.toprettyxml()
    xml = minidom.parseString(ElementTree.tostring(h4)) # or xml.dom.minidom.parseString(xml_string)
    h4_string = xml.toprettyxml()
    xml = minidom.parseString(ElementTree.tostring(table)) # or xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = xml.toprettyxml()

    formattedContentTest = "{0} {1} {2}".format(h3_String, h4_string, pretty_xml_as_string)

    #formattedContent.append(ElementTree.Comment(' --><![CDATA[' + data.replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))
    formattedContent.text =  '<![CDATA[' + formattedContentTest.replace(']]>', ']]]]><![CDATA[>') + ']]>'

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

xml = minidom.parseString(ElementTree.tostring(root)) # or xml.dom.minidom.parseString(xml_string)
pretty_xml_as_string = xml.toprettyxml()
#print pretty_xml_as_string

formattedXmlToWrite = escape(pretty_xml_as_string)

output_file.write(formattedXmlToWrite)
output_file.close()
