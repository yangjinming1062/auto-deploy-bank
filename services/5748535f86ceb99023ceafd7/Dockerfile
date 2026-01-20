# Multi-stage build for metasfresh-webui-api

# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy misc directory first (parent POMs and assemblies)
COPY misc/ ./misc/

# Install de.metas.parent.general to local repository first
RUN mvn install:install-file -Dfile=misc/parent-pom/pom.xml \
    -DgroupId=de.metas \
    -DartifactId=de.metas.parent.general \
    -Dversion=10.0.0 \
    -Dpackaging=pom \
    -DgeneratePom=false \
    -DpomFile=misc/parent-pom/pom.xml \
    -B

# Copy backend pom.xml to correct location and then copy backend sources
COPY backend/pom.xml ./backend/pom.xml
COPY backend/ ./backend/

# Build de-metas-common modules
WORKDIR /build/misc/de-metas-common
RUN mvn install:install-file -Dfile=pom.xml \
    -DgroupId=de.metas.common \
    -DartifactId=de-metas-common \
    -Dversion=10.0.0 \
    -Dpackaging=pom \
    -B && \
    mvn install -DskipTests -B -Dmaven.gitcommitid.skip=true

# Install metasfresh-assemblies
WORKDIR /build
RUN mvn install:install-file -Dfile=misc/parent-pom/assemblies/pom.xml \
    -DgroupId=de.metas \
    -DartifactId=metasfresh-assemblies \
    -Dversion=10.0.0 \
    -Dpackaging=pom \
    -B && \
    mkdir -p /tmp/assemblies-jar && \
    echo '<assembly xmlns="http://maven.apache.org/ASSEMBLY/2.0.0"><id>dummy</id><formats><format>jar</format></formats></assembly>' > /tmp/assemblies-jar/dummy.xml && \
    (cd /tmp/assemblies-jar && jar cf metasfresh-assemblies-10.0.0.jar dummy.xml) && \
    mvn install:install-file -Dfile=/tmp/assemblies-jar/metasfresh-assemblies-10.0.0.jar \
        -DgroupId=de.metas \
        -DartifactId=metasfresh-assemblies \
        -Dversion=10.0.0 \
        -Dpackaging=jar \
        -DpomFile=/build/misc/parent-pom/assemblies/pom.xml \
        -B

# Build de.metas.assemblies
WORKDIR /build/backend/de.metas.assemblies
RUN mvn install -DskipTests -B -Dmaven.gitcommitid.skip=true

# Install jpedal stub - using printf to avoid truncation issues
RUN mkdir -p /tmp/jpedal/org/jpedal && \
    printf 'package org.jpedal;\npublic class PdfPageData {\n    public int getRotation(int p) { return 0; }\n}\n' > /tmp/jpedal/org/jpedal/PdfPageData.java && \
    printf 'package org.jpedal;\nimport java.awt.*;\nimport java.awt.print.*;\npublic class PdfDecoder extends Component implements Pageable, Printable {\n    public static final int TEXTGLYPHPRINT = 0;\n    private PdfPageData pd = new PdfPageData();\n    public PdfDecoder() {}\n    public void setPdfFile(String f) {}\n    public void openPdfFile(String f) {}\n    public void closePdf() {}\n    public void closePdfFile() {}\n    public Object getPageAsImage(int p) { return null; }\n    public int getPageCount() { return 1; }\n    public void decodePage(int p) {}\n    public void setPageParameters(float s, int p) {}\n    public void setPageParameters(float s, int p, int r) {}\n    public void setTextPrint(int m) {}\n    public PdfPageData getPdfPageData() { return pd; }\n    public void setPageFormat(PageFormat pf) {}\n    public void invalidate() {}\n    public void repaint() {}\n    public int getNumberOfPages() { return 1; }\n    public PageFormat getPageFormat(int i) { return new PageFormat(); }\n    public Printable getPrintable(int i) { return this; }\n    public int print(Graphics g, PageFormat pf, int i) { return NO_SUCH_PAGE; }\n}\n' > /tmp/jpedal/org/jpedal/PdfDecoder.java && \
    cd /tmp/jpedal && javac org/jpedal/PdfDecoder.java org/jpedal/PdfPageData.java && jar cf jpedal-1.0.jar org/jpedal/*.class && \
    mvn install:install-file -Dfile=jpedal-1.0.jar -DgroupId=org.jpedal -DartifactId=jpedal -Dversion=1.0 -Dpackaging=jar -B

# Install pdf-renderer stub (used by printing.client) with com.sun.pdfview package
RUN mkdir -p /tmp/pdf-renderer/com/sun/pdfview && \
    printf 'package com.sun.pdfview;\nimport java.awt.geom.*;\nimport java.awt.image.*;\nimport java.nio.ByteBuffer;\nimport java.io.IOException;\npublic class PDFFile {\n    public PDFFile(byte[] data) throws IOException {}\n    public PDFFile(ByteBuffer bb) throws IOException {}\n    public int getNumPages() { return 1; }\n    public PDFPage getPage(int pageNum) { return new PDFPage(); }\n}\n' > /tmp/pdf-renderer/com/sun/pdfview/PDFFile.java && \
    printf 'package com.sun.pdfview;\nimport java.awt.*;\nimport java.awt.geom.*;\npublic class PDFPage {\n    public Rectangle2D getBBox() { return new Rectangle2D.Float(0, 0, 100, 100); }\n    public Rectangle2D getPageBox() { return new Rectangle2D.Float(0, 0, 100, 100); }\n    public double getWidth() { return 100.0; }\n    public double getHeight() { return 100.0; }\n    public Dimension getUnstretchedSize(int widthLimit, int heightLimit, Rectangle2D pageBox) { return new Dimension(100, 100); }\n    public void render(Graphics2D g) {}\n    public void dispose() {}\n    public void waitForFinish() throws InterruptedException {}\n}\n' > /tmp/pdf-renderer/com/sun/pdfview/PDFPage.java && \
    printf 'package com.sun.pdfview;\nimport java.awt.*;\nimport java.awt.geom.*;\nimport java.awt.image.*;\npublic class PDFRenderer {\n    private PDFPage pdfPage;\n    private Graphics2D g2d;\n    private Rectangle2D bounds;\n    public PDFRenderer(PDFPage pdfPage, Graphics2D g2d, Rectangle2D bounds, Rectangle2D clip, Color bgColor) {\n        this.pdfPage = pdfPage;\n        this.g2d = g2d;\n        this.bounds = bounds;\n    }\n    public PDFRenderer(PDFFile file) {}\n    public void renderPage(int page, Graphics2D g) {}\n    public int getPageCount() { return 1; }\n    public BufferedImage getPageImage(int page) { return new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB); }\n    public void dispose() {}\n    public void run() throws InterruptedException {}\n}\n' > /tmp/pdf-renderer/com/sun/pdfview/PDFRenderer.java && \
    cd /tmp/pdf-renderer && javac com/sun/pdfview/*.java && jar cf pdf-renderer-0.9.0.jar com/sun/pdfview/*.class && \
    mvn install:install-file -Dfile=pdf-renderer-0.9.0.jar -DgroupId=net.dev.java -DartifactId=pdf-renderer -Dversion=0.9.0 -Dpackaging=jar -B

# Install font stubs for metasfresh-report-service
RUN mkdir -p /tmp/fonts/de/metas/report/jasper && \
    mkdir -p /tmp/fonts/de/metas/report/jasper/cantarellfonts && \
    printf 'package de.metas.report.jasper.cantarellfonts;\npublic class CantarellFonts {\n    public static java.awt.Font getFont() { return java.awt.Font.decode("Dialog"); }\n}\n' > /tmp/fonts/de/metas/report/jasper/cantarellfonts/CantarellFonts.java && \
    mkdir -p /tmp/fonts/de/metas/report/jasper/montserratfonts && \
    printf 'package de.metas.report.jasper.montserratfonts;\npublic class MontserratFonts {\n    public static java.awt.Font getFont() { return java.awt.Font.decode("Dialog"); }\n}\n' > /tmp/fonts/de/metas/report/jasper/montserratfonts/MontserratFonts.java && \
    mkdir -p /tmp/fonts/de/metas/report/jasper/robotofonts && \
    printf 'package de.metas.report.jasper.robotofonts;\npublic class RobotoFonts {\n    public static java.awt.Font getFont() { return java.awt.Font.decode("Dialog"); }\n}\n' > /tmp/fonts/de/metas/report/jasper/robotofonts/RobotoFonts.java && \
    mkdir -p /tmp/fonts/de/metas/report/jasper/opensansfonts && \
    printf 'package de.metas.report.jasper.opensansfonts;\npublic class OpenSansFonts {\n    public static java.awt.Font getFont() { return java.awt.Font.decode("Dialog"); }\n}\n' > /tmp/fonts/de/metas/report/jasper/opensansfonts/OpenSansFonts.java && \
    mkdir -p /tmp/fonts/de/metas/report/jasper/sourcecodeprofonts && \
    printf 'package de.metas.report.jasper.sourcecodeprofonts;\npublic class SourceCodeProFonts {\n    public static java.awt.Font getFont() { return java.awt.Font.decode("Monospaced"); }\n}\n' > /tmp/fonts/de/metas/report/jasper/sourcecodeprofonts/SourceCodeProFonts.java && \
    cd /tmp/fonts && find . -name "*.java" -exec javac {} + && \
    jar cf cantarell-fonts-001.001.jar de/metas/report/jasper/cantarellfonts/*.class && \
    jar cf montserrat-fonts-8.000.jar de/metas/report/jasper/montserratfonts/*.class && \
    jar cf roboto-fonts-2012023.1-2.jar de/metas/report/jasper/robotofonts/*.class && \
    jar cf open-sans-fonts-1.10.jar de/metas/report/jasper/opensansfonts/*.class && \
    jar cf source-code-pro-fonts-1.0.0.jar de/metas/report/jasper/sourcecodeprofonts/*.class && \
    mvn install:install-file -Dfile=cantarell-fonts-001.001.jar -DgroupId=de.metas.report.jasper -DartifactId=cantarell-fonts -Dversion=001.001 -Dpackaging=jar -B && \
    mvn install:install-file -Dfile=montserrat-fonts-8.000.jar -DgroupId=de.metas.report.jasper -DartifactId=montserrat-fonts -Dversion=8.000 -Dpackaging=jar -B && \
    mvn install:install-file -Dfile=roboto-fonts-2012023.1-2.jar -DgroupId=de.metas.report.jasper -DartifactId=roboto-fonts -Dversion=2012023.1-2 -Dpackaging=jar -B && \
    mvn install:install-file -Dfile=open-sans-fonts-1.10.jar -DgroupId=de.metas.report.jasper -DartifactId=open-sans-fonts -Dversion=1.10 -Dpackaging=jar -B && \
    mvn install:install-file -Dfile=source-code-pro-fonts-1.0.0.jar -DgroupId=de.metas.report.jasper -DartifactId=source-code-pro-fonts -Dversion=1.0.0 -Dpackaging=jar -B

# Create git directories for git-commit-id-plugin
WORKDIR /build
RUN mkdir -p /build/.git/refs/heads && \
    echo "ref: refs/heads/master" > /build/.git/HEAD && \
    printf "0123456789abcdef0123456789abcdef01234567" > /build/.git/refs/heads/master && \
    echo "[core]" > /build/.git/config && echo "repositoryformatversion=0" >> /build/.git/config && \
    echo "filemode=false" >> /build/.git/config && echo "bare=false" >> /build/.git/config && \
    mkdir -p /build/backend/de.metas.adempiere.adempiere/tools/.git/refs/heads && \
    echo "ref: refs/heads/master" > /build/backend/de.metas.adempiere.adempiere/tools/.git/HEAD && \
    printf "0123456789abcdef0123456789abcdef01234567" > /build/backend/de.metas.adempiere.adempiere/tools/.git/refs/heads/master

# Build from backend directory (where pom.xml is in correct relative location)
# Build only metasfresh-webui-api and its dependencies
WORKDIR /build/backend
RUN mvn install -DskipTests -B -Dmaven.gitcommitid.skip=true -Dmetasfresh.version=10.0.0 \
    -Dassembly.skipAssembly=true \
    -Ddocker.build.directory=/build/backend/metasfresh-webui-api/target \
    -pl metasfresh-webui-api -am

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache curl
WORKDIR /app
COPY --from=builder /build/backend/metasfresh-webui-api/target/metasfresh-webui-api.jar target.jar
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 CMD curl -f http://localhost:8080/health || exit 1
CMD ["java", "-Xmx512M", "-XX:+HeapDumpOnOutOfMemoryError", "-Dsun.misc.URLClassPath.disableJarChecking=true", "-Dspring.data.elasticsearch.cluster-nodes=${ES_HOST:-search}:${ES_PORT:-9300}", "-Dspring.rabbitmq.host=${RABBITMQ_HOST:-rabbitmq}", "-Dspring.rabbitmq.port=${RABBITMQ_PORT:-5672}", "-Dspring.rabbitmq.username=${RABBITMQ_USER:-metasfresh}", "-Dspring.rabbitmq.password=${RABBITMQ_PASSWORD:-metasfresh}", "-Dloader.path=/opt/metasfresh/external-lib", "-DPropertyFile=/app/metasfresh.properties", "-Djava.security.egd=file:/dev/./urandom", "-jar", "target.jar"]