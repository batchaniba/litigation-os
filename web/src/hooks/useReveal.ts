import { useEffect, useRef } from "react";

export function useReveal<T extends HTMLElement = HTMLElement>(rootMargin = "0px 0px -8% 0px") {
  const ref = useRef<T | null>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      node.classList.add("is-visible");
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          node.classList.add("is-visible");
          observer.disconnect();
        }
      },
      { rootMargin, threshold: 0.15 },
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [rootMargin]);

  return ref;
}
