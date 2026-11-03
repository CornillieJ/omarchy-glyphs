import QtQuick
import qs.Commons

Row {
  id: bar

  property var labels: []
  property int current: 0
  property color foreground
  property color selectedBackground
  property color selectedText
  property string fontFamily
  property int cornerRadius: Style.cornerRadius

  signal picked(int index)

  spacing: Style.spacing.md

  Repeater {
    model: bar.labels

    Rectangle {
      required property int index
      required property string modelData

      readonly property bool active: index === bar.current

      width: (bar.width - bar.spacing * (bar.labels.length - 1)) / bar.labels.length
      height: bar.height
      radius: bar.cornerRadius
      color: active ? bar.selectedBackground : "transparent"

      Text {
        textFormat: Text.PlainText
        anchors.centerIn: parent
        text: parent.modelData
        color: parent.active ? bar.selectedText : bar.foreground
        opacity: parent.active ? 1 : 0.6
        font.family: bar.fontFamily
        font.pixelSize: Style.font.title
      }

      MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: bar.picked(parent.index)
      }
    }
  }
}
