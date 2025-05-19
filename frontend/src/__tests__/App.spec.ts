// frontend/src/__tests__/App.spec.ts
import { render } from '@testing-library/svelte'
import { describe, it, expect } from 'vitest'
import App from '../App.svelte'

describe('App.svelte', () => {
  it('mounts without crashing', () => {
    const { container } = render(App)
    expect(container).toBeTruthy()
  })
})
