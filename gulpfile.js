var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var cleanCSS = require('gulp-clean-css');


gulp.task('sass', function() {
    return gulp.src('kyleinprogress/scss/sass/app.scss')
        .pipe(sass())
        .pipe(autoprefixer({ browsers: ['last 2 version'] }))
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(gulp.dest('kyleinprogress/static/css/'));

});

gulp.task('copy-files', function () {
    gulp.src('node_modules/bootstrap-sass/assets/fonts/bootstrap/**')
        .pipe(gulp.dest('kyleinprogress/static/fonts'));
    gulp.src('node_modules/font-awesome/fonts/**')
        .pipe(gulp.dest('kyleinprogress/static/fonts'));
});

gulp.task('default', ['sass', 'copy-files']);
