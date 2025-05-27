import { test, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/svelte'
import Content from '../Content.svelte'

// Create mock data in the exact shape processData() expects
const mockArticles = [
  {
    _id: '1',
    headline: { main: 'Hello World' },
    abstract: 'Summary',
    multimedia: { caption: '', default: { url: '' } },
    web_url: 'https://example.com',
    word_count: 450
  }
]

beforeEach(() => {
  // Stub global fetch to intercept all network calls  
  vi.stubGlobal('fetch', vi.fn((input: RequestInfo) => {
    const url = typeof input === 'string' ? input : input.toString()
    if (url.endsWith('/api/userinfo')) {
      // Return a fake user response for loadUser()
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ email: 'a@b.com', name: 'Tester' })
      })
    }
    if (url.endsWith('/api/ucdavis-news')) {
      // Return our mock articles for the news API
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ response: { docs: mockArticles } })
      })
    }
    // any other fetch (e.g. comments) — just return an empty payload
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({})
    })
  }))
})

test('Content loads and displays articles', async () => {
  render(Content)

  // Wait for the headline to appear in the DOM
  expect(await screen.findByText('Hello World')).toBeInTheDocument()
  // The read time: Math.ceil(450/150) === 3 → "3 MIN READ"
  expect(await screen.findByText('3 MIN READ')).toBeInTheDocument()
})
