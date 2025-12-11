/**
 * FooterContent Component - Brand footer with social links and TiltCheck CTA
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import React from 'react';
import { FaLinkedin, FaEnvelope, FaHeart, FaGithub } from 'react-icons/fa';
import { SiKofi } from 'react-icons/si';

export default function FooterContent() {
  return (
    <div className="mt-auto border-t border-neon-pink/20 bg-dark-bg/50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-8 border-b border-neon-pink/10">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-2xl font-bold text-white mb-2 neon-glow">Check Out TiltCheck</h3>
          <p className="text-gray-400 mb-4 max-w-2xl mx-auto">
            A comprehensive poker tracking and analytics platform built for serious players. Track sessions,
            analyze performance, manage bankroll, and eliminate tilt with real-time insights and AI-powered
            recommendations.
          </p>
          <a
            href="https://tiltcheck.me"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-neon-pink/10 border border-neon-pink text-neon-pink rounded-lg hover:bg-neon-pink hover:text-dark-bg transition-all duration-300 neon-glow-hover group"
          >
            <span className="font-semibold">Visit TiltCheck</span>
            <svg
              className="w-5 h-5 transform group-hover:translate-x-1 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </a>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="text-gray-400 text-sm mb-1">&copy; 2025 Jmenichole. All rights reserved.</p>
            <div className="flex flex-col md:flex-row items-center gap-3">
              <a
                href="https://jmenichole.github.io/Portfolio/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-300 hover:text-neon-pink transition-colors duration-300 text-sm inline-flex items-center gap-2 group"
              >
                Made for degens by degens
                <FaHeart className="text-neon-pink animate-pulse group-hover:scale-110 transition-transform" />
              </a>
              <span className="text-gray-600 hidden md:inline">•</span>
              <a
                href="https://www.ncpgambling.org/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-500 hover:text-neon-cyan transition-colors duration-300 text-xs"
              >
                🎲 Responsible Gaming Resources
              </a>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <a
              href="https://ko-fi.com/jmenichole0"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-[#FF5E5B] transition-colors duration-300 hover:scale-110 transform"
              aria-label="Support on Ko-fi"
            >
              <SiKofi className="text-2xl neon-glow-hover" />
            </a>
            <a
              href="https://linkedin.com/in/jmenichole0"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-neon-pink transition-colors duration-300 hover:scale-110 transform"
              aria-label="LinkedIn Profile"
            >
              <FaLinkedin className="text-2xl neon-glow-hover" />
            </a>
            <a
              href="mailto:jme@tiltcheck.me"
              className="text-gray-400 hover:text-neon-pink transition-colors duration-300 hover:scale-110 transform"
              aria-label="Email Contact"
            >
              <FaEnvelope className="text-2xl neon-glow-hover" />
            </a>
            <a
              href="https://github.com/jmenichole"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-neon-pink transition-colors duration-300 hover:scale-110 transform"
              aria-label="GitHub Profile"
            >
              <FaGithub className="text-2xl neon-glow-hover" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
