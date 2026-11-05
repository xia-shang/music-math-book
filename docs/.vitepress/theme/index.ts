import DefaultTheme from 'vitepress/theme'
import ConsonanceExplorer from './components/ConsonanceExplorer.vue'
import CentsRuler from './components/CentsRuler.vue'
import Box from './components/Box.vue'
import Figure from './components/Figure.vue'
import AudioDemo from './components/AudioDemo.vue'
import EuclideanRhythmLab from './components/EuclideanRhythmLab.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ConsonanceExplorer', ConsonanceExplorer)
    app.component('CentsRuler', CentsRuler)
    app.component('Box', Box)
    app.component('Figure', Figure)
    app.component('AudioDemo', AudioDemo)
    app.component('EuclideanRhythmLab', EuclideanRhythmLab)
  }
}
