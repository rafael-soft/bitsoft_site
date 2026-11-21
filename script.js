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

// Formulário de contato via Web3Forms (https://web3forms.com, plano gratuito).
// Cole aqui a Access Key recebida por e-mail. Enquanto estiver vazia, o envio
// abre o programa de e-mail do visitante com a mensagem preenchida.
const WEB3FORMS_ACCESS_KEY = 'e4931133-3f82-46eb-925b-1302bb3079fb';
const CONTACT_EMAIL = 'contato@bitsoft.dev.br';

const contactForm = document.getElementById('contact-form');

if (contactForm) {
  const status = contactForm.querySelector('.form-status');
  const submitButton = contactForm.querySelector('button[type="submit"]');

  const setStatus = (message, type) => {
    status.textContent = message;
    status.className = `form-status ${type || ''}`;
  };

  const validate = () => {
    let firstInvalid = null;
    contactForm.querySelectorAll('[required]').forEach((field) => {
      const valid = field.value.trim() !== '' && field.checkValidity();
      field.classList.toggle('invalid', !valid);
      field.setAttribute('aria-invalid', String(!valid));
      if (!valid && !firstInvalid) firstInvalid = field;
    });
    if (firstInvalid) firstInvalid.focus();
    return !firstInvalid;
  };

  contactForm.addEventListener('input', (event) => {
    if (event.target.classList.contains('invalid') && event.target.checkValidity()) {
      event.target.classList.remove('invalid');
      event.target.setAttribute('aria-invalid', 'false');
    }
  });

  contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!validate()) {
      setStatus('Preencha nome, e-mail válido e mensagem.', 'error');
      return;
    }

    const data = Object.fromEntries(new FormData(contactForm));

    if (!WEB3FORMS_ACCESS_KEY) {
      const body = `Nome: ${data.name}\nE-mail: ${data.email}\nTelefone: ${data.phone || '-'}\nProjeto: ${data.project_type}\n\n${data.message}`;
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(`Contato pelo site — ${data.project_type}`)}&body=${encodeURIComponent(body)}`;
      return;
    }

    submitButton.disabled = true;
    setStatus('Enviando…');

    try {
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          ...data,
          access_key: WEB3FORMS_ACCESS_KEY,
          subject: `Contato pelo site — ${data.project_type}`,
          from_name: 'Site Bitsoft',
          replyto: data.email,
          botcheck: Boolean(data.botcheck),
        }),
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.message);

      contactForm.reset();
      setStatus('Mensagem enviada! Retornaremos em breve.', 'success');
    } catch (error) {
      setStatus(`Não foi possível enviar agora. Tente novamente ou escreva para ${CONTACT_EMAIL}.`, 'error');
    } finally {
      submitButton.disabled = false;
    }
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
