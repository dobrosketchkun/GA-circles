"GA-circles" представляет собой небольшой эксперимент для выяснения возможности использовая генетических алгоритмов для игр.
Конкретно здесь происходи отбор (ну, вернее будет, пока его ещё нет) кругов, идущих по лабиринту. Нужно дойти до его конца до окончания времени раунда, после чего происходят разные ГА-штуки и следущее поколение пытается снова и так далее.

TODO:
 Добавить пусть из экземпляров специального класса,которые будут по правильному пути располагаться. При взаимодействии они должны исчезать, а счётчик
коллизий увеличиваться. Это позволит уменьшить "примагничивание" генома к локальному минимуму, если старт и финиш в абсолютных
значениях располагаюся близко друг к другу, но между ними много стен.
