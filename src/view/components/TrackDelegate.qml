import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: trackDelegate
    height: 50
    color: index % 2 ? "#2a2a2a" : "#252525"

    property bool isSelected: false
    signal selectedChanged()

    RowLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        CheckBox {
            checked: isSelected
            onCheckedChanged: {
                isSelected = checked
                selectedChanged()
            }
        }

        Text { 
            text: title
            color: "white"
            Layout.fillWidth: true 
        }

        Text { 
            text: artist
            color: "white"
            Layout.fillWidth: true 
        }

        Text { 
            text: album
            color: "white"
            Layout.fillWidth: true 
        }

        Text { 
            text: year
            color: "white"
            Layout.preferredWidth: 80 
        }

        Text { 
            text: duration
            color: "white"
            Layout.preferredWidth: 100 
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            isSelected = !isSelected
            selectedChanged()
        }
        hoverEnabled: true
        onEntered: parent.color = Qt.lighter(parent.color, 1.1)
        onExited: parent.color = index % 2 ? "#2a2a2a" : "#252525"
    }
}