import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: playerControlsRoot
    height: 100
    color: "#1e1e1e"

    property real currentPosition: 0
    property real duration: 0
    property int volume: 100
    property bool isPlaying: false
    property string currentTrack: "No track selected"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5

        // Información de la pista actual
        Text {
            text: currentTrack
            color: "white"
            font.pixelSize: 14
            Layout.alignment: Qt.AlignHCenter
        }

        // Barra de progreso
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: formatTime(currentPosition)
                color: "white"
                font.pixelSize: 12
            }

            Slider {
                id: progressSlider
                Layout.fillWidth: true
                from: 0
                to: duration
                value: currentPosition
                onMoved: controller.seek(value)

                background: Rectangle {
                    height: 4
                    color: "#444444"
                    Rectangle {
                        width: progressSlider.visualPosition * parent.width
                        height: parent.height
                        color: "#1db954"
                    }
                }
            }

            Text {
                text: formatTime(duration)
                color: "white"
                font.pixelSize: 12
            }
        }

        // Controles de reproducción
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 20

            Button {
                icon.source: "qrc:/icons/previous.svg"
                onClicked: controller.previousTrack()
            }

            Button {
                icon.source: isPlaying ? "qrc:/icons/pause.svg" : "qrc:/icons/play.svg"
                onClicked: controller.playPause()
            }

            Button {
                icon.source: "qrc:/icons/next.svg"
                onClicked: controller.nextTrack()
            }

            // Control de volumen
            RowLayout {
                spacing: 10

                Button {
                    icon.source: volume === 0 ? "qrc:/icons/mute.svg" : "qrc:/icons/volume.svg"
                    onClicked: controller.toggleMute()
                }

                Slider {
                    id: volumeSlider
                    from: 0
                    to: 100
                    value: volume
                    onMoved: controller.setVolume(value)
                    
                    background: Rectangle {
                        height: 4
                        color: "#444444"
                        Rectangle {
                            width: volumeSlider.visualPosition * parent.width
                            height: parent.height
                            color: "#1db954"
                        }
                    }
                }
            }
        }
    }

    // Función auxiliar para formateo de tiempo
    function formatTime(seconds) {
        let minutes = Math.floor(seconds / 60)
        let secs = Math.floor(seconds % 60)
        return minutes.toString().padStart(2, '0') + ":" + 
               secs.toString().padStart(2, '0')
    }
}