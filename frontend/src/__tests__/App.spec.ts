import { render, screen } from '@testing-library/svelte'
import App from '../App.svelte'

describe('App.svelte', () => {
  it('mounts without crashing', () => {
  render(App)
  // if it doesn’t throw, we’re good
})
})

