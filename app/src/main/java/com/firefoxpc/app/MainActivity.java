package com.firefoxpc.app;

import android.Manifest;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class MainActivity extends Activity {

    static final String TAG     = "FirefoxPC";
    // نستخدم مسار الـ cache أولاً كـ fallback إذا فشل الـ external storage
    String LOG_DIR;

    String appDataDir = "/data/data/com.firefoxpc.app";
    String appPrefix;
    String appHome;
    String activePrefix;

    static final String[] TERMUX_PREFIXES = {
        "/data/data/com.termux/files/usr",
        "/data/data/com.termux.fdroid/files/usr",
    };

    TextView    tvStatus;
    ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle s) {
        super.onCreate(s);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                             WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_main);
        tvStatus    = findViewById(R.id.tvStatus);
        progressBar = findViewById(R.id.progressBar);

        appPrefix = appDataDir + "/files/usr";
        appHome   = appDataDir + "/files/home";

        // إعداد LOG_DIR — نجرّب external أولاً ثم internal
        String extLog = "/storage/emulated/0/Download/FirefoxPC_Logs/";
        File extDir = new File(extLog);
        if (extDir.exists() || extDir.mkdirs()) {
            LOG_DIR = extLog;
        } else {
            // fallback: internal storage
            LOG_DIR = getFilesDir().getAbsolutePath() + "/logs/";
            new File(LOG_DIR).mkdirs();
        }

        flog("=== Firefox PC Started ===");
        flog("Android " + Build.VERSION.RELEASE + " / " + Build.SUPPORTED_ABIS[0]);
        flog("LOG_DIR=" + LOG_DIR);
        flog("appPrefix=" + appPrefix);
        flog("cacheDir=" + getCacheDir());

        // طلب permission للـ storage (Android 6+)
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{
                    Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    Manifest.permission.READ_EXTERNAL_STORAGE
                }, 1);
            }
        }

        // Phantom process killer fix (Android 12+)
        if (Build.VERSION.SDK_INT >= 31) {
            try { new ProcessBuilder("/system/bin/settings","put","global",
                "settings_enable_monitor_phantom_procs","false").start().waitFor();
                flog("Phantom killer disabled");
            } catch (Exception e) { flog("Phantom killer: " + e.getMessage()); }
        }

        Intent svc = new Intent(this, BgService.class);
        if (Build.VERSION.SDK_INT >= 26) startForegroundService(svc);
        else startService(svc);

        new Thread(this::setup).start();
    }

    void setup() {
        try {
            new File(appHome).mkdirs();
            new File(appPrefix).mkdirs();

            // ── 1. ابحث عن Termux ────────────────────────────────
            status("Checking environment...", 3);
            activePrefix = findTermux();

            // ── 2. Bootstrap ──────────────────────────────────────
            if (activePrefix == null) {
                File bash = new File(appPrefix + "/bin/bash");
                if (bash.exists()) {
                    flog("Bootstrap already extracted");
                    activePrefix = appPrefix;
                } else {
                    status("Extracting tools...", 5);
                    if (extractBootstrap()) {
                        activePrefix = appPrefix;
                    } else {
                        status("❌ Bootstrap failed — see app.log", -1);
                        return;
                    }
                }
            }

            // ── 3. اختبر bash ──────────────────────────────────────
            status("Testing bash...", 9);
            String[] testResult = testBash(activePrefix + "/bin/bash");
            flog("bash method: " + testResult[0]);
            flog("bash output: " + testResult[1]);

            if (testResult[0].equals("FAIL")) {
                status("❌ bash failed: " + testResult[1], -1);
                return;
            }
            flog("✅ bash works via: " + testResult[0]);

            // ── 4. السكريبتات ──────────────────────────────────────
            status("Preparing scripts...", 12);
            extractScripts();

            // ── 5. setup أو start ──────────────────────────────────
            File done = new File(appHome, ".setup_complete");
            if (!done.exists()) {
                status("Extracting system files...", 15);
                extractSystemParts();
                status("Setting up Ubuntu (3-5 min)...", 40);
                runScript("scripts/setup.sh", "setup.log");
            } else {
                status("Starting Firefox...", 80);
                runScript("scripts/start.sh", "start.log");
            }

            new Handler(Looper.getMainLooper()).postDelayed(
                () -> moveTaskToBack(true), 5000);

        } catch (Exception e) {
            flog("SETUP EXCEPTION: " + e.getClass().getSimpleName() + ": " + e.getMessage());
            for (StackTraceElement el : e.getStackTrace()) flog("  " + el);
            status("❌ Error: " + e.getMessage(), -1);
        }
    }

    // ── استخراج bootstrap من assets ──────────────────────────
    boolean extractBootstrap() {
        flog("--- extractBootstrap ---");
        try {
            String[] files = getAssets().list("bootstrap");
            flog("bootstrap assets count: " + (files == null ? "null" : files.length));
            if (files == null || files.length == 0) {
                flog("No bootstrap assets!"); return false;
            }
            for (String f : files) flog("  " + f);

            File tmpZip = new File(getCacheDir(), "bs.zip");

            boolean hasParts = false;
            for (String f : files) if (f.contains(".part")) { hasParts=true; break; }

            if (hasParts) {
                Arrays.sort(files);
                try (FileOutputStream out = new FileOutputStream(tmpZip)) {
                    for (String p : files) {
                        if (!p.contains(".part")) continue;
                        flog("  joining: " + p);
                        try (InputStream in = getAssets().open("bootstrap/" + p)) {
                            byte[] buf = new byte[65536]; int n;
                            while ((n=in.read(buf))>0) out.write(buf,0,n);
                        }
                    }
                }
            } else {
                String fname = files[0];
                flog("Extracting single file: " + fname);
                try (InputStream in = getAssets().open("bootstrap/" + fname);
                     FileOutputStream out = new FileOutputStream(tmpZip)) {
                    byte[] buf = new byte[65536]; int n;
                    while ((n=in.read(buf))>0) out.write(buf,0,n);
                }
            }
            flog("Zip size: " + tmpZip.length()/1024/1024 + "MB");
            boolean ok = extractZip(tmpZip);
            tmpZip.delete();
            return ok;
        } catch (Exception e) {
            flog("extractBootstrap error: " + e.getMessage()); return false;
        }
    }

    boolean extractZip(File zipFile) {
        flog("extractZip → " + appPrefix);
        new File(appPrefix).mkdirs();
        List<String[]> symlinks = new ArrayList<>();
        int count = 0;
        try (ZipInputStream zis = new ZipInputStream(new java.io.FileInputStream(zipFile))) {
            ZipEntry e;
            while ((e = zis.getNextEntry()) != null) {
                String name = e.getName();
                if (name.equals("SYMLINKS.txt")) {
                    BufferedReader br = new BufferedReader(new InputStreamReader(zis));
                    String line;
                    while ((line=br.readLine()) != null) {
                        String[] p = line.split("←");
                        if (p.length==2) symlinks.add(p);
                    }
                    zis.closeEntry(); continue;
                }
                File out = new File(appPrefix, name);
                if (e.isDirectory()) { out.mkdirs(); zis.closeEntry(); continue; }
                out.getParentFile().mkdirs();
                try (FileOutputStream fos = new FileOutputStream(out)) {
                    byte[] buf = new byte[32768]; int n;
                    while ((n=zis.read(buf))>0) fos.write(buf,0,n);
                }
                if (name.startsWith("bin/") || name.contains("/bin/") ||
                    name.endsWith(".sh")   || name.startsWith("libexec/"))
                    out.setExecutable(true,false);
                count++;
                zis.closeEntry();
            }
        } catch (Exception e) { flog("extractZip error: "+e.getMessage()); return false; }

        flog("Files: " + count);
        for (String[] sl : symlinks) {
            try {
                File link = new File(appPrefix, sl[0].trim());
                link.getParentFile().mkdirs();
                if (link.exists()) link.delete();
                android.system.Os.symlink(sl[1].trim(), link.getAbsolutePath());
            } catch (Exception ignored) {}
        }
        flog("Symlinks: " + symlinks.size());
        File bash = new File(appPrefix+"/bin/bash");
        bash.setExecutable(true,false);
        flog("bash: exists="+bash.exists()+" exec="+bash.canExecute());
        return bash.exists();
    }

    // ── اختبار bash — يجرّب طريقتين ──────────────────────────
    // returns [method, output]
    String[] testBash(String bash) {
        flog("testBash: " + bash);
        flog("  exists=" + new File(bash).exists());
        flog("  canExec=" + new File(bash).canExecute());

        // طريقة 1: مباشر
        try {
            java.lang.Process p = new ProcessBuilder(bash, "-c", "echo BASH_OK_$$")
                .redirectErrorStream(true).start();
            String out = new BufferedReader(new InputStreamReader(p.getInputStream())).readLine();
            int code = p.waitFor();
            flog("  direct: exit="+code+" out="+out);
            if (code==0 && out!=null && out.startsWith("BASH_OK"))
                return new String[]{"DIRECT", out};
        } catch (Exception e) { flog("  direct exc: "+e.getMessage()); }

        // طريقة 2: عبر /system/bin/sh (يتجاوز noexec)
        try {
            java.lang.Process p = new ProcessBuilder(
                "/system/bin/sh", "-c", bash + " -c 'echo BASH_OK_$$'")
                .redirectErrorStream(true).start();
            String out = new BufferedReader(new InputStreamReader(p.getInputStream())).readLine();
            int code = p.waitFor();
            flog("  via sh: exit="+code+" out="+out);
            if (code==0 && out!=null && out.startsWith("BASH_OK"))
                return new String[]{"VIA_SH", out};
        } catch (Exception e) { flog("  via sh exc: "+e.getMessage()); }

        return new String[]{"FAIL", "cannot execute bash"};
    }

    void runScript(String rel, String logFile) {
        File script = new File(appHome, rel);
        String bash = activePrefix + "/bin/bash";
        flog("runScript: "+rel+" (log→"+logFile+")");
        flog("  script exists: "+script.exists());
        flog("  bash: "+bash+" exists="+new File(bash).exists());

        new Thread(() -> {
            try {
                // /system/bin/sh لتجاوز noexec
                ProcessBuilder pb = new ProcessBuilder(
                    "/system/bin/sh", "-c",
                    "\"" + bash + "\" \"" + script.getAbsolutePath() + "\"");
                pb.environment().put("HOME",    appHome);
                pb.environment().put("PREFIX",  activePrefix);
                pb.environment().put("TERM",    "xterm-256color");
                pb.environment().put("TMPDIR",  getCacheDir().getAbsolutePath());
                pb.environment().put("PATH",
                    activePrefix+"/bin:"+activePrefix+"/sbin:/system/bin:/system/xbin");
                // LD_PRELOAD لـ libtermux-exec.so (يساعد في exec داخل bash)
                File ldp = new File(activePrefix+"/lib/libtermux-exec.so");
                if (ldp.exists()) {
                    pb.environment().put("LD_PRELOAD", ldp.getAbsolutePath());
                    flog("  LD_PRELOAD: "+ldp);
                }
                pb.redirectErrorStream(true);
                pb.directory(new File(appHome));

                java.lang.Process p = pb.start();
                flog("Script PID started");

                BufferedReader br = new BufferedReader(
                    new InputStreamReader(p.getInputStream()));
                String line;
                while ((line=br.readLine()) != null) {
                    final String l = line;
                    flogTo(logFile, l);
                    new Handler(Looper.getMainLooper()).post(() -> tvStatus.setText(l));
                }
                int exit = p.waitFor();
                flog("Script exit=" + exit + " file="+rel);

                if (exit == 0 && rel.contains("setup")) {
                    // إنشاء ملف done
                    new File(appHome, ".setup_complete").createNewFile();
                    flog("Setup complete marker created");
                    new Handler(Looper.getMainLooper()).post(
                        () -> status("Starting Firefox...", 80));
                    Thread.sleep(1000);
                    runScript("scripts/start.sh", "start.log");
                }
            } catch (Exception e) {
                flog("runScript ERROR: "+e.getMessage());
                status("Script error: "+e.getMessage(), -1);
            }
        }).start();
    }

    String findTermux() {
        for (String prefix : TERMUX_PREFIXES) {
            File bash = new File(prefix+"/bin/bash");
            flog("Check: "+bash+" e="+bash.exists());
            if (bash.exists()) {
                String[] t = testBash(bash.getAbsolutePath());
                flog("  result: "+t[0]);
                if (!t[0].equals("FAIL")) return prefix;
            }
        }
        return null;
    }

    void extractScripts() throws IOException {
        File sd = new File(appHome, "scripts"); sd.mkdirs();
        for (String name : new String[]{"setup.sh","start.sh"}) {
            String c = readAssetText("scripts/"+name);
            c = c.replace("__PREFIX__", activePrefix)
                 .replace("/data/data/com.termux/files/usr", activePrefix)
                 .replace("/data/data/com.firefoxpc.app/files/usr", activePrefix);
            if (c.startsWith("#!")) {
                int nl = c.indexOf('\n');
                c = "#!" + activePrefix + "/bin/bash\n" + c.substring(nl+1);
            }
            File f = new File(sd, name);
            writeText(f, c); f.setExecutable(true,false);
            flog("Script ready: "+name+" ("+c.length()+" bytes)");
        }
    }

    void extractSystemParts() throws IOException {
        File sysDir = new File(appHome, "assets/system"); sysDir.mkdirs();
        String[] parts = getAssets().list("system");
        if (parts==null||parts.length==0) { flog("No system parts!"); return; }
        int idx=0;
        for (String part : parts) {
            if (part.equals("README.txt")||part.equals("manifest.txt")) continue;
            idx++;
            status("Part "+idx+"/"+parts.length+": "+part, 15+idx*55/parts.length);
            File dst = new File(sysDir, part);
            if (dst.exists()&&dst.length()>1024*1024) { flog("Skip existing: "+part); continue; }
            copyAsset("system/"+part, dst);
            flog("Part done: "+part+" "+dst.length()/1024/1024+"MB");
        }
    }

    // ── Utilities ─────────────────────────────────────────────
    void copyAsset(String a, File d) throws IOException {
        try (InputStream in=getAssets().open(a); FileOutputStream out=new FileOutputStream(d)) {
            byte[] buf=new byte[65536]; int n;
            while((n=in.read(buf))>0) out.write(buf,0,n);
        }
    }
    String readAssetText(String a) throws IOException {
        try (InputStream in=getAssets().open(a); InputStreamReader r=new InputStreamReader(in)) {
            StringBuilder sb=new StringBuilder(); char[] buf=new char[4096]; int n;
            while((n=r.read(buf))>0) sb.append(buf,0,n); return sb.toString();
        }
    }
    void writeText(File d, String c) throws IOException {
        d.getParentFile().mkdirs();
        try (FileOutputStream f=new FileOutputStream(d);
             OutputStreamWriter w=new OutputStreamWriter(f)) { w.write(c); }
    }
    String ts() { return new SimpleDateFormat("HH:mm:ss.SSS",Locale.US).format(new Date()); }
    void flog(String msg) {
        Log.d(TAG, msg);
        try { new File(LOG_DIR).mkdirs();
            try(FileOutputStream f=new FileOutputStream(LOG_DIR+"app.log",true);
                OutputStreamWriter w=new OutputStreamWriter(f)){w.write("["+ts()+"] "+msg+"\n");}
        }catch(Exception ignored){}
    }
    void flogTo(String file, String msg) {
        try { new File(LOG_DIR).mkdirs();
            try(FileOutputStream f=new FileOutputStream(LOG_DIR+file,true);
                OutputStreamWriter w=new OutputStreamWriter(f)){
                w.write("["+ts().substring(0,8)+"] "+msg+"\n");}
        }catch(Exception ignored){}
    }
    void status(String msg, int pct) {
        flog("STATUS["+pct+"%]: "+msg);
        new Handler(Looper.getMainLooper()).post(()->{
            tvStatus.setText(msg);
            if(pct>=0){progressBar.setProgress(pct);progressBar.setVisibility(View.VISIBLE);}
        });
    }

    public static class BgService extends Service {
        static final String CH="ffpc",EXIT="com.firefoxpc.app.EXIT";static final int NID=1;
        @Override public int onStartCommand(Intent i,int f,int s){
            if(i!=null&&EXIT.equals(i.getAction())){
                try{Runtime r=Runtime.getRuntime();
                    r.exec(new String[]{"pkill","-f","firefox"});
                    r.exec(new String[]{"pkill","-f","termux.x11"});
                    r.exec(new String[]{"pkill","-f","pulseaudio"});
                }catch(Exception ignored){}
                stopSelf();android.os.Process.killProcess(android.os.Process.myPid());
                return START_NOT_STICKY;
            }
            mkCh();startForeground(NID,notif());return START_STICKY;
        }
        Notification notif(){
            Intent ei=new Intent(this,BgService.class);ei.setAction(EXIT);
            PendingIntent ep=PendingIntent.getService(this,0,ei,
                PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
            Notification.Builder b=Build.VERSION.SDK_INT>=26
                ?new Notification.Builder(this,CH):new Notification.Builder(this);
            return b.setContentTitle("Firefox PC").setContentText("Running")
                .setSmallIcon(R.mipmap.ic_launcher)
                .addAction(android.R.drawable.ic_delete,"Exit",ep)
                .setOngoing(true).setPriority(Notification.PRIORITY_MIN).build();
        }
        void mkCh(){if(Build.VERSION.SDK_INT>=26)
            getSystemService(NotificationManager.class).createNotificationChannel(
                new NotificationChannel(CH,"Firefox PC",NotificationManager.IMPORTANCE_MIN));}
        @Override public IBinder onBind(Intent i){return null;}
    }
}
