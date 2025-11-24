import { defineConfig } from 'vite';

export default defineConfig({
      
      build: {
        rollupOptions: {
          output: {
            // Specify the name for the main JavaScript bundle
            entryFileNames: 'index.js', 
            // Specify the name for the main CSS bundle
            assetFileNames: 'style.css', 
            // Disable chunking to ensure a single JS file
            manualChunks: () => 'everything.js',
            
            
          }
        }
      }
    });