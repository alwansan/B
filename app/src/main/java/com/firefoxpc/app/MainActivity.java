package com.firefoxpc.app;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class MainActivity extends Activity {

    private static final String TAG = "FirefoxPC";
    private static final String SETUP_DONE = ".setup_complete";
    private TextView tvStatus;
    private ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Fullscreen immersive
        getWindow().addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON |
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            View.SYSTEM_UI_FLAG_FULLSCREEN |
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );

        setContentView(R.layout.activity_main);
        tvStatus  = findViewById(R.id.tvStatus);
        progressBar = findViewById(R.id.progressBar);

        // Start persistent notification service
        Intent svc = new Intent(this, BgService.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            startForegroundService(svc);
        else
            startService(svc);

        new Thread(this::run).start();
    }

    private void run() {
        try {
            File homeDir = new File(getDataDir(), "files/home");
            homeDir.mkdirs();

            status("Extracting scripts...", 10);
            extractScripts(homeDir);

            File setupDone = new File(homeDir, SETUP_DONE);
            if (!setupDone.exists()) {
                status("First launch — extracting system (2-4 min)...", 20);
                extractSystemParts(homeDir);
                status("Setting up Ubuntu...", 40);
                runScript(homeDir, "scripts/setup.sh");
            } else {
                status("Starting Firefox...", 80);
                runScript(homeDir, "scripts/start.sh");
            }

            new Handler(Looper.getMainLooper()).postDelayed(
                () -> moveTaskToBack(true), 3000);

        } catch (Exception e) {
            Log.e(TAG, "Error", e);
            status("Error: " + e.getMessage(), -1);
        }
    }

    private void extractScripts(File homeDir) throws IOException {
        File scriptsDir = new File(homeDir, "scripts");
        scriptsDir.mkdirs();
        for (String name : new String[]{"setup.sh", "start.sh"}) {
            File dest = new File(scriptsDir, name);
            copyAsset("scripts/" + name, dest);
            dest.setExecutable(true, false);
        }
        // Also copy into assets folder so setup.sh can find them
        File assetsScripts = new File(homeDir, "assets/scripts");
        assetsScripts.mkdirs();
        for (String name : new String[]{"setup.sh", "start.sh"}) {
            copyAsset("scripts/" + name, new File(assetsScripts, name));
        }
    }

    private void extractSystemParts(File homeDir) throws IOException {
        File sysDir = new File(homeDir, "assets/system");
        sysDir.mkdirs();
        String[] parts = getAssets().list("system");
        if (parts == null || parts.length == 0) return;
        int i = 0;
        for (String part : parts) {
            i++;
            status("Extracting part " + i + "/" + parts.length + "...",
                   20 + (i * 20 / parts.length));
            copyAsset("system/" + part, new File(sysDir, part));
        }
    }

    private void copyAsset(String asset, File dest) throws IOException {
        try (InputStream in  = getAssets().open(asset);
             FileOutputStream out = new FileOutputStream(dest)) {
            byte[] buf = new byte[16384];
            int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
        }
    }

    private void runScript(File homeDir, String rel) {
        try {
            File script = new File(homeDir, rel);
            ProcessBuilder pb = new ProcessBuilder(
                "/data/data/com.firefoxpc.app/files/usr/bin/bash",
                script.getAbsolutePath()
            );
            pb.environment().put("HOME",   homeDir.getAbsolutePath());
            pb.environment().put("PREFIX", getDataDir() + "/files/usr");
            pb.environment().put("TERM",   "xterm-256color");
            pb.environment().put("TMPDIR", getCacheDir().getAbsolutePath());
            pb.redirectErrorStream(true);

            Process p = pb.start();
            BufferedReader br = new BufferedReader(
                new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = br.readLine()) != null) {
                final String l = line;
                Log.d(TAG, l);
                new Handler(Looper.getMainLooper()).post(() -> tvStatus.setText(l));
            }
            p.waitFor();
        } catch (Exception e) {
            Log.e(TAG, "Script error", e);
        }
    }

    private void status(String msg, int prog) {
        new Handler(Looper.getMainLooper()).post(() -> {
            tvStatus.setText(msg);
            if (prog >= 0) {
                progressBar.setProgress(prog);
                progressBar.setVisibility(View.VISIBLE);
            }
        });
    }

    // ── Background Service + Exit Notification ───────────────────────────────
    public static class BgService extends Service {
        static final String CH  = "ffpc_ch";
        static final int    NID = 1;
        static final String EXIT = "com.firefoxpc.app.EXIT";

        @Override
        public int onStartCommand(Intent i, int f, int s) {
            if (i != null && EXIT.equals(i.getAction())) {
                try {
                    Runtime r = Runtime.getRuntime();
                    r.exec(new String[]{"pkill", "-f", "firefox"});
                    r.exec(new String[]{"pkill", "-f", "termux.x11"});
                    r.exec(new String[]{"pkill", "-f", "pulseaudio"});
                } catch (Exception ignored) {}
                stopSelf();
                android.os.Process.killProcess(android.os.Process.myPid());
                return START_NOT_STICKY;
            }
            mkChannel();
            startForeground(NID, buildNotif());
            return START_STICKY;
        }

        Notification buildNotif() {
            Intent ei = new Intent(this, BgService.class);
            ei.setAction(EXIT);
            int flags = PendingIntent.FLAG_UPDATE_CURRENT |
                        PendingIntent.FLAG_IMMUTABLE;
            PendingIntent ep = PendingIntent.getService(this, 0, ei, flags);

            Notification.Builder b = Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(this, CH)
                : new Notification.Builder(this);

            return b.setContentTitle("Firefox PC")
                    .setContentText("Running in background")
                    .setSmallIcon(R.mipmap.ic_launcher)
                    .addAction(android.R.drawable.ic_delete, "Exit", ep)
                    .setOngoing(true)
                    .build();
        }

        void mkChannel() {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                NotificationChannel c = new NotificationChannel(
                    CH, "Firefox PC", NotificationManager.IMPORTANCE_LOW);
                getSystemService(NotificationManager.class)
                    .createNotificationChannel(c);
            }
        }

        @Override public IBinder onBind(Intent i) { return null; }
    }
}
