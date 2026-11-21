// Número do WhatsApp com DDI e DDD, só dígitos (ex.: '5511999999999').
// Enquanto estiver vazio, os botões de WhatsApp ficam ocultos.
const WHATSAPP_NUMBER = '5511975604128';
const WHATSAPP_MESSAGE = 'Olá! Vim pelo site da Bitsoft e gostaria de conversar sobre um projeto.';

if (WHATSAPP_NUMBER) {
  const href = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`;
  document.querySelectorAll('[data-whatsapp]').forEach((link) => {
    link.href = href;
    link.target = '_blank';
    link.rel = 'noopener';
    link.hidden = false;
  });
}

// Menu mobile
const menuToggle = document.querySelector('.menu-toggle');
const menu = document.getElementById('menu');

const setMenu = (open) => {
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  document.body.classList.toggle('menu-open', open);
};

menuToggle.addEventListener('click', () => {
  setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
});

menu.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setMenu(false);
});

// Header com fundo ao rolar
const topbar = document.querySelector('.topbar');
const onScroll = () => topbar.classList.toggle('scrolled', window.scrollY > 12);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Ano no rodapé
document.getElementById('ano').textContent = new Date().getFullYear();

// Animação de entrada dos blocos
const revealElements = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.15,
  }
);

revealElements.forEach((element) => {
  const siblings = [...element.parentElement.children].filter((el) => el.classList.contains('reveal'));
  element.style.transitionDelay = `${siblings.indexOf(element) * 70}ms`;
  observer.observe(element);
});
