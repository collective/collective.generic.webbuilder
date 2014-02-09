var gulp = require('gulp');
var sass = require('gulp-ruby-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var less = require('gulp-less');
var jshint = require('gulp-jshint');
var uglify = require('gulp-uglify');
var imagemin = require('gulp-imagemin');
var rename = require('gulp-rename');
var debug = require('gulp-debug');
var clean = require('gulp-clean');
var concat = require('gulp-concat');
var notify = require('gulp-notify');
var cache = require('gulp-cache');
var b = './src/collective/generic/webbuilder/templates/';
var d = './src/collective/generic/webbuilder/templates/static/';
var addond = "./src/collective.generic.skel/src/collective/generic/skel/addon/tmpl/+namespace++ndot++nested_namespace++nsdot++project_name+/src/+namespace+/+nested_namespace+/+project_name+/static_bootstrap/"
var csss = ['./bower_components/bootstrap/dist/css/bootstrap.css',
        './bower_components/font-awesome/css/font-awesome.css',
        b+'theme.css'];
var javascripts = ['./bower_components/jquery/jquery.js',
                   './bower_components/bootstrap/dist/js/bootstrap.js',
                   b+'theme.js'];
var addon_csss = [addond+'less/+project_name+.less'];
w = process.cwd();
styles = gulp.task(
    'styles',
    function() {
        return gulp.src(csss)
        .pipe(concat('style.css'))
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
        .pipe(gulp.dest(d+'css/'))
        .pipe(notify({message: 'Styles task complete'}))
        .pipe(minifycss())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(d+'css/'))
        .pipe(notify({message: 'Styles task min complete'}));
    });
js = gulp.task(
    'js',
    function() {
        return gulp.src(javascripts)
        .pipe(concat('script.js'))
        .pipe(gulp.dest(d+'js/'))
        .pipe(uglify())
        .pipe(rename('script.min.js'))
        .pipe(gulp.dest(d+'js/'))
        .pipe(notify({message: 'JS task complete'}));
    });
fonts = gulp.task(
    'fonts',
    function() {
        return gulp.src([
            './bower_components/font-awesome/fonts/**',
        ])
        .pipe(gulp.dest(d+'fonts/'))
        .pipe(notify({message: 'FONTS task complete'}));
    });
addon_styles = gulp.task(
    'addon_styles',
    function() {
        return gulp.src(addon_csss)
        .pipe(less(''))
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
        .pipe(rename("theme.css"))
        .pipe(gulp.dest(addond+'css/'))
        .pipe(notify({message: 'Styles task complete'}))
        .pipe(minifycss())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(addond+'css/'))
        .pipe(notify({message: 'Styles task min complete'}));
    });
gulp.task('default', ['js', 'styles', 'fonts', 'addon_styles']);
gulp.task('watch', function() {
  gulp.watch(addon_csss, ['addon_styles']);
  gulp.watch(csss, ['styles']);
  gulp.watch(javascripts, ['js']);
});
