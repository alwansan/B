#!/bin/sh
##############################################################################
# Gradle start up script for UN*X
##############################################################################
set -e
APP_HOME="$(cd "$(dirname "$0")" && pwd -P)"
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

if [ -n "$JAVA_HOME" ] ; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

# Check java is available
which "$JAVACMD" >/dev/null 2>&1 || {
    echo "ERROR: JAVA_HOME is not set and no 'java' found in PATH." >&2
    exit 1
}

CLASSPATH="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"

exec "$JAVACMD" \
    $DEFAULT_JVM_OPTS \
    $JAVA_OPTS \
    $GRADLE_OPTS \
    -classpath "$CLASSPATH" \
    org.gradle.wrapper.GradleWrapperMain \
    "$@"
